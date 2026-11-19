import { spawn } from 'node:child_process';
import { access, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { constants } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import assert from 'node:assert/strict';
import { indexWalkthrough } from './smoke_index_browser.mjs';
import { transactionWalkthrough } from './smoke_transaction_browser.mjs';
// Run against a disposable workspace only.
function testOrigin(value) {
  const url = new URL(value);
  assert.equal(url.protocol, 'http:');
  assert.ok(['localhost', '127.0.0.1'].includes(url.hostname) && url.port && !['3000', '8080', '3001', '8081'].includes(url.port));
  return url.origin;
}
const frontendOrigin = testOrigin(process.env.SQL_TEST_FRONTEND_ORIGIN ?? 'http://localhost:13000');
const apiOrigin = testOrigin(process.env.SQL_TEST_API_ORIGIN ?? 'http://localhost:18080');
const chromePath=process.env.SQL_TEST_CHROME || (process.platform==='darwin'
  ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' : '/usr/bin/google-chrome');
await access(chromePath, constants.X_OK).catch(()=>{throw new Error('Chrome unavailable: set SQL_TEST_CHROME to its executable path.');});
const profile=await mkdtemp(join(tmpdir(),'pythoria-phase8a-chrome-'));
const chrome=spawn(chromePath,[
  '--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check',
  '--remote-debugging-port=0',`--user-data-dir=${profile}`,'about:blank',
],{stdio:['ignore','ignore','pipe']});
let ws;
try {
  const endpoint=await new Promise((resolve,reject)=>{
    let log='';const timer=setTimeout(()=>reject(new Error('Chrome startup timeout')),20000);
    chrome.stderr.on('data',chunk=>{log+=chunk;const match=log.match(/DevTools listening on (ws:\/\/[^\s]+)/);if(match){clearTimeout(timer);resolve(match[1]);}});
    chrome.once('error',reject);
    chrome.on('exit',code=>reject(new Error('Chrome exited '+code)));
  });
  ws=new WebSocket(endpoint);
  await new Promise((resolve,reject)=>{ws.addEventListener('open',resolve,{once:true});ws.addEventListener('error',reject,{once:true});});
  let sequence=0,sessionId;
  const pending=new Map();
  ws.addEventListener('message',event=>{const msg=JSON.parse(event.data);if(msg.id){const p=pending.get(msg.id);if(p){pending.delete(msg.id);msg.error?p.reject(new Error(JSON.stringify(msg.error))):p.resolve(msg.result);}}});
  function call(method,params={},session=sessionId){return new Promise((resolve,reject)=>{const id=++sequence;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params,...(session?{sessionId:session}:{})}));});}
  const {targetId}=await call('Target.createTarget',{url:'about:blank'});
  ({sessionId}=await call('Target.attachToTarget',{targetId,flatten:true}));
  await call('Page.enable');await call('Runtime.enable');
  await call('Page.bringToFront');
  await call('Emulation.setFocusEmulationEnabled',{enabled:true});
  await call('Network.enable');
  await call('Network.setBlockedURLs',{urls:['http://localhost:8080/*','http://127.0.0.1:8080/*','http://localhost:3000/*','http://127.0.0.1:3000/*','http://localhost:3001/*','http://127.0.0.1:3001/*','http://localhost:8081/*','http://127.0.0.1:8081/*']});
  async function evaluate(expression){const r=await call('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;}
  async function until(expression,timeout=60000){const end=Date.now()+timeout;do{try{if(await evaluate(`Boolean((${expression}))`))return;}catch(e){if(!/context|Cannot find/i.test(e.message))throw e;}await new Promise(r=>setTimeout(r,150));}while(Date.now()<end);throw new Error('Timed out: '+expression+'\n'+await evaluate('document.body.innerText.slice(-1800)'));}
  async function click(selector){await evaluate(`document.querySelector(${JSON.stringify(selector)}).click()`);}
  async function key(key,code,keyCode,modifiers=0){const text=key==='Enter'&&modifiers===0?{text:'\r',unmodifiedText:'\r'}:{};await call('Input.dispatchKeyEvent',{type:'keyDown',key,code,windowsVirtualKeyCode:keyCode,modifiers,...text});await call('Input.dispatchKeyEvent',{type:'keyUp',key,code,windowsVirtualKeyCode:keyCode,modifiers:0});}
  async function type(selector,text){
    await call('Page.bringToFront');
    if(selector.includes('textarea')){
      const parent=selector.includes('.sql-editor')?'.sql-editor':'.editor-panel';
      await evaluate(`(()=>{const editor=window.__phase8aMonaco.editor.getEditors().find(e=>e.getDomNode()?.closest(${JSON.stringify(parent)}));if(!editor)throw new Error('No mounted Monaco editor');editor.focus();editor.setSelection(editor.getModel().getFullModelRange());return true;})()`);
    }else{
      await evaluate(`(()=>{const input=document.querySelector(${JSON.stringify(selector)});input.focus({preventScroll:true});input.select();return true;})()`);
    }
    await call('Input.insertText',{text});
  }
  async function typePython(source){
    // CDP's multiline insertText is interpreted as typing by Monaco and can
    // reindent subsequent lines. Enter one line at a time with native events;
    // select only the indentation produced by Enter before typing that line.
    const editor=`window.__phase8aMonaco.editor.getEditors().find(e=>e.getDomNode()?.closest('.editor-panel'))`;
    // Enter must insert a newline even when a completion is available.
    const configure=`e.updateOptions({
      autoIndent:'none', autoClosingBrackets:'never', autoClosingQuotes:'never',
      autoClosingComments:'never', formatOnType:false, formatOnPaste:false,
      acceptSuggestionOnEnter:'off', quickSuggestions:false, suggestOnTriggerCharacters:false,
    });`;
    await call('Page.bringToFront');
    await evaluate(`(()=>{const e=${editor};e.focus();e.setSelection(e.getModel().getFullModelRange());${configure}return true;})()`);
    await key('Backspace','Backspace',8);
    await until(`(${editor}).getModel().getValue()===''`);
    const lines=source.split('\n');
    for(let index=0;index<lines.length;index++){
      await evaluate(`(()=>{const e=${editor};e.focus();${configure}return true;})()`);
      if(index)await key('Enter','Enter',13);
      const indentationLength=await evaluate(`(()=>{const e=${editor},p=e.getPosition(),line=e.getModel().getLineContent(p.lineNumber);if(line.trim())throw new Error('Unexpected content before native line ${index}: '+JSON.stringify({position:p,line,value:e.getModel().getValue()}));e.setSelection({startLineNumber:p.lineNumber,startColumn:1,endLineNumber:p.lineNumber,endColumn:line.length+1});${configure}return line.length;})()`);
      if(lines[index])await call('Input.insertText',{text:lines[index]});
      else if(indentationLength)await key('Backspace','Backspace',8);
      const prefix=lines.slice(0,index+1).join('\n');
      await until(`(${editor}).getModel().getValue()===${JSON.stringify(prefix)}`);
    }
  }
  async function shortcut(check=false){await evaluate(`(()=>{window.__phase8aMonaco.editor.getEditors().find(e=>e.getDomNode()?.closest('.sql-editor')).focus();return true;})()`);await key('Enter','Enter',13,check?12:4);}
  // The runner intentionally rejects a concurrent reaper operation with 409.
  // Retry only that explicit pre-execution busy response, never Failed/SQL errors.
  async function submit(check,ready){
    for(let attempt=0;attempt<5;attempt++){
      await until(`!document.querySelector('${check?'.check-button':'.run-button'}').disabled`);
      await shortcut(check);
      await new Promise(resolve=>setTimeout(resolve,200));
      await until(`document.querySelector('.sql-footer')?.textContent.includes('сессия активна') && ((${ready}) || document.querySelector('.sql-connection-error')!==null || document.querySelector('.sql-diagnostic')!==null || ${check?"document.querySelector('.sql-check-feedback.failed')!==null":"false"})`,check?120000:60000);
      if(await evaluate(ready))return;
      const message=await evaluate(`document.querySelector('.sql-connection-error')?.textContent || document.querySelector('.sql-diagnostic')?.textContent || document.querySelector('.sql-check-feedback.failed')?.textContent || ''`);
      if(!message.includes('занята') || attempt===4)throw new Error('SQL UI submission failed: '+message);
      await new Promise(resolve=>setTimeout(resolve,500));
    }
  }
  async function size(width,height,mobile=false){await call('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile});}
  async function screenshot(path){const shot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await writeFile(path,Buffer.from(shot.data,'base64'));}
  async function api(path,data,method){return evaluate(`fetch(${JSON.stringify(apiOrigin)}+${JSON.stringify(path)},{method:${JSON.stringify(method|| (data?'POST':'GET'))},headers:{'Content-Type':'application/json'},${data?'body:'+JSON.stringify(JSON.stringify(data))+',':''}}).then(async r=>{if(!r.ok)throw new Error('HTTP '+r.status);return r.status===204?null:r.json()})`);}
  async function stage11Walkthrough() {
    await until(`document.querySelector('.lesson-title-row h1')?.textContent==='JSONB' && document.body.innerText.includes('jsonb_set')`);
    await until(`document.querySelector('.postgres-examples')?.innerText.includes('scripts/test_stage11_examples.sh')`);
    assert.equal(await evaluate(`document.querySelector('.workspace-pane .check-button')===null`), true);
    const hiddenJsonb = () => evaluate(`Array.from(document.querySelectorAll('details')).filter(d=>['Раскрыть ответы','Раскрыть критерии'].includes(d.querySelector('summary')?.textContent)).map(d=>d.open)`);
    assert.deepEqual(await hiddenJsonb(), [false,false]);
    await evaluate(`Array.from(document.querySelectorAll('.lesson-mode-switch button')).find(b=>b.textContent.includes('Повторение')).click()`);
    assert.deepEqual(await hiddenJsonb(), [false,false]);
    await evaluate(`Array.from(document.querySelectorAll('.lesson-mode-switch button')).find(b=>b.textContent.includes('Обучение')).click()`);
    await evaluate(`document.querySelector('.lesson-reader').scrollTop=0`);
    await screenshot('/tmp/pythoria-phase9b-jsonb-desktop.png');
    await size(390,844,true);
    await until(`document.querySelector('.course-sidebar').getBoundingClientRect().right<=0`);
    assert.equal(await evaluate(`document.documentElement.scrollWidth<=window.innerWidth`),true);
    await screenshot('/tmp/pythoria-phase9b-jsonb-mobile.png');
    await size(1720,1050);
    await until(`document.querySelector('.course-sidebar').getBoundingClientRect().left>=-0.5`);
    console.log(JSON.stringify({stage11Jsonb:true,learnReviewAnswersClosed:true,mobile390:true}));
  }
  await size(1720,1050);
  if (process.argv.includes('--stage11-only')) {
    await call('Page.navigate', {url: frontendOrigin + '/?lesson=s11-jsonb'});
    await stage11Walkthrough();
    await call('Target.closeTarget', {targetId}, null);
  } else {
  await call('Page.navigate',{url:frontendOrigin + '/?lesson=s10-select-aliases-and-expressions'});
  await until(`typeof window.require==='function' && document.querySelector('.sql-footer')?.textContent.includes('сессия активна')`);
  await evaluate(`new Promise((resolve,reject)=>window.require(['vs/editor/editor.main'],loaded=>{window.__phase8aMonaco=loaded.m||loaded;resolve(true)},reject))`);
  const pythonFiles={'main.py':"def compare_objects(a, b):\n    return {'same_identity': a is b, 'same_value': a == b}\n",'notes.py':"PRESERVED = 'phase8a-browser'\n"};
  await api('/api/lessons/is-vs-eq/files',{files:pythonFiles},'PUT');
  const pythonLesson=await api('/api/lessons/is-vs-eq');
  const selfLesson=await api('/api/lessons/s10-self-join');
  const tasks=[
    ['s10-select-aliases-and-expressions','sql.guided.10.2.projection.v1','SELECT id AS user_id,email FROM users'],
    ['s10-where-and-boolean-logic','sql.basic.01','SELECT id,email FROM users WHERE active=true'],
    ['s10-null-and-three-valued-logic','sql.basic.03','SELECT id,email FROM users WHERE country IS NULL'],
    ['s10-order-by-limit-and-offset','sql.basic.04','SELECT id,created_at FROM orders ORDER BY created_at DESC,id DESC LIMIT 2'],
    ['s10-distinct','sql.basic.05','SELECT DISTINCT country FROM users WHERE country IS NOT NULL ORDER BY country'],
    ['s10-aggregates','sql.aggregation.09','SELECT COUNT(*) AS orders_count FROM orders'],
    ['s10-group-by','sql.aggregation.10','SELECT status,COUNT(*) AS count FROM orders GROUP BY status ORDER BY status'],
    ['s10-having','sql.aggregation.13','SELECT user_id,COUNT(*) AS count FROM orders GROUP BY user_id HAVING COUNT(*)>=2 ORDER BY user_id'],
    ['s10-inner-join','sql.join.17','SELECT o.id AS order_id,u.email FROM orders o JOIN users u ON u.id=o.user_id ORDER BY o.id'],
    ['s10-left-join','sql.join.18','SELECT u.id,u.email FROM users u LEFT JOIN orders o ON o.user_id=u.id WHERE o.id IS NULL'],
    ['s10-right-and-full-outer-join','sql.join.25','SELECT p.id AS product_id,oi.order_id FROM order_items oi RIGHT JOIN products p ON p.id=oi.product_id ORDER BY p.id,oi.order_id'],
    ['s10-self-join','sql.join.20','SELECT u.email,m.email AS manager_email FROM users u LEFT JOIN users m ON m.id=u.manager_id ORDER BY u.id'],
    ["s10-subqueries", "sql.subquery.27", "SELECT id,total FROM orders WHERE total > (SELECT AVG(total) FROM orders)"],
    ["s10-correlated-subquery", "sql.subquery.31", "SELECT o.id,o.user_id FROM orders o WHERE o.created_at=(SELECT MAX(i.created_at) FROM orders i WHERE i.user_id=o.user_id) ORDER BY o.user_id"],
    ["s10-exists-vs-in", "sql.subquery.28", "SELECT u.id,u.email FROM users u WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id=u.id AND o.status='paid')"],
    ["s10-cte", "sql.subquery.30", "WITH paid_totals AS (SELECT user_id,SUM(total) revenue FROM orders WHERE status='paid' GROUP BY user_id) SELECT user_id,revenue FROM paid_totals WHERE revenue>=150 ORDER BY user_id"],
    ["s10-recursive-cte", "sql.subquery.32", "WITH RECURSIVE chain AS (SELECT id,manager_id,0 depth FROM users WHERE id=4 UNION ALL SELECT u.id,u.manager_id,c.depth+1 FROM users u JOIN chain c ON u.id=c.manager_id) SELECT id,depth FROM chain ORDER BY depth"],
    ["s10-case", "sql.basic.06", "SELECT id, CASE status WHEN 'paid' THEN 'completed' WHEN 'cancelled' THEN 'cancelled' ELSE 'pending' END AS label FROM orders"],
    ["s10-set-operations", "sql.set.50", "SELECT country FROM users WHERE active EXCEPT SELECT u.country FROM users u JOIN orders o ON o.user_id=u.id WHERE o.status='paid' ORDER BY country NULLS LAST"],
    ["s10-window-functions", "sql.window.37", "SELECT id,user_id,total,LAG(total) OVER(PARTITION BY user_id ORDER BY created_at,id) AS previous_total FROM orders ORDER BY user_id,created_at,id"],
    ["s10-row-number-rank-dense-rank", "sql.window.33", "SELECT id,user_id,ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY created_at DESC,id DESC) AS row_number FROM orders ORDER BY user_id,row_number"],
    ["s10-partition-by-and-window-ordering", "sql.window.36", "SELECT id,user_id,SUM(total) OVER(PARTITION BY user_id ORDER BY created_at,id) AS running_total FROM orders ORDER BY user_id,created_at,id"],
    ["s10-lag-and-lead", "sql.window.38", "SELECT id,user_id,LEAD(created_at) OVER(PARTITION BY user_id ORDER BY created_at,id) AS next_created_at FROM orders ORDER BY user_id,created_at,id"],

  ];
  async function selectLesson(title,slug){
    await type('.lesson-search input',title);
    await until(`Array.from(document.querySelectorAll('button.lesson')).some(b=>b.textContent.includes(${JSON.stringify(title)}))`);
    await evaluate(`Array.from(document.querySelectorAll('button.lesson')).find(b=>b.textContent.includes(${JSON.stringify(title)})).click()`);
    await until(`new URLSearchParams(location.search).get('lesson')===${JSON.stringify(slug)}`);
  }
  if (process.argv.includes('--index-only')) {
    await indexWalkthrough({api,evaluate,until,selectLesson,call,size,screenshot});
    await call('Target.closeTarget',{targetId},null);
  } else if(process.argv.includes('--transactions-only')){
    await transactionWalkthrough({api,evaluate,until,selectLesson,call,size,screenshot});
    await call('Target.closeTarget',{targetId},null);
  } else {
  const counts=[4,5,5,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6];
  for(let i=0;i<tasks.length;i++){
    const [slug,task,query]=tasks[i];
    await until(`new URLSearchParams(location.search).get('lesson')===${JSON.stringify(slug)} && window.__phase8aMonaco.editor.getModels().some(m=>m.uri.toString().includes(${JSON.stringify(task)})) && document.querySelector('.sql-footer')?.textContent.includes('сессия активна')`);
    assert.equal((await api('/api/sql/lessons/'+slug)).completed,false);
    await type('.sql-editor textarea',query);
    await until(`window.__phase8aMonaco.editor.getModels().find(m=>m.uri.toString().includes(${JSON.stringify(task)})).getValue()===${JSON.stringify(query)}`);
    await submit(false, `document.querySelector('.sql-output table[aria-label="Результат PostgreSQL"]')!==null`);
    assert.equal((await api('/api/sql/lessons/'+slug)).completed,false);
    const draft=await evaluate(`localStorage.getItem(Object.keys(localStorage).find(k=>k.startsWith('pythoria:sql:')&&k.endsWith(${JSON.stringify(task)})))`);
    assert.equal(draft,query);
    const layout=await evaluate(`(()=>{const e=document.querySelector('.sql-editor'),o=document.querySelector('.sql-output');return {editor:getComputedStyle(e).display,output:getComputedStyle(o).display,editorHeight:e.getBoundingClientRect().height,outputHeight:o.getBoundingClientRect().height};})()`);
    assert.notEqual(layout.editor,'none');assert.notEqual(layout.output,'none');assert(layout.editorHeight>30&&layout.outputHeight>30);
    if(i>=8){
      const disclosed=await evaluate(`Array.from(document.querySelectorAll('details')).filter(d=>d.querySelector('summary')?.textContent==='Показать решение для самопроверки').map(d=>d.open)`);
      assert.deepEqual(disclosed,[false]);
      await evaluate(`Array.from(document.querySelectorAll('button')).find(b=>b.textContent.includes('Повторение')).click()`);
      assert.deepEqual(await evaluate(`Array.from(document.querySelectorAll('details')).filter(d=>d.querySelector('summary')?.textContent==='Показать решение для самопроверки').map(d=>d.open)`),[false]);
      await evaluate(`Array.from(document.querySelectorAll('button')).find(b=>b.textContent.includes('Обучение')).click()`);
    }
    await submit(true, `document.querySelector('.sql-check-feedback.passed')?.textContent.includes('${counts[i]} / ${counts[i]}') && document.querySelector('.sql-task-completed')!==null`);
    assert.equal((await api('/api/sql/lessons/'+slug)).completed,true);
    console.log(JSON.stringify({slug,task,actualMonacoTyping:true,run:true,check:`${counts[i]}/${counts[i]}`,draft:true,desktopEditorAndResults:true}));
    if(i<tasks.length-1)await evaluate(`Array.from(document.querySelectorAll('.lesson-navigation button')).find(b=>b.textContent.trim()==='Далее').click()`);
  }
  assert.equal((await api('/api/course')).summary.xp,0);
  await click('[role="tab"][id$="-database"]');
  await until(`document.querySelector('.sql-schema')?.textContent.includes('manager_id') && document.querySelector('.sql-relationships')?.textContent.includes('users')`);
  await click('[role="tab"][id$="-editor"]');
  await screenshot('/tmp/pythoria-phase8a-desktop.png');
  const oldTheme=await evaluate(`document.querySelector('.course-app').classList.contains('dark')`);
  await click('[aria-label="Сменить тему"]');
  await until(`document.querySelector('.course-app').classList.contains('dark')!==${oldTheme}`);
  await until(`document.querySelector('.monaco-editor.${oldTheme?'vs':'vs-dark'}')!==null`);
  await screenshot('/tmp/pythoria-phase8a-light.png');
  await size(390,844,true);
  await until(`document.querySelector('.course-sidebar').getBoundingClientRect().right<=0 && getComputedStyle(document.querySelector('.sql-sidebar')).display==='none'`);
  assert.equal(await evaluate(`getComputedStyle(document.querySelector('.sql-output')).display`),'none');
  await click('[role="tab"][id$="-results"]');
  await until(`getComputedStyle(document.querySelector('.sql-output')).display!=='none' && document.querySelector('.sql-output table')!==null`);
  assert.equal(await evaluate(`document.documentElement.scrollWidth<=window.innerWidth`),true);
  const tableSpace=await evaluate(`(()=>{const viewport=document.querySelector('.sql-table-scroll').getBoundingClientRect();const table=document.querySelector('.sql-table-scroll table');const header=table.tHead.getBoundingClientRect();const row=table.tBodies[0].rows[0].getBoundingClientRect();return {bodySpace:viewport.bottom-header.bottom,rowHeight:row.height};})()`);
  assert(tableSpace.bodySpace>=2*tableSpace.rowHeight, 'Mobile results must expose at least two complete rows: '+JSON.stringify(tableSpace));
  await screenshot('/tmp/pythoria-phase8a-mobile.png');
  await size(1720,1050);
  await until(`document.querySelector('.course-sidebar').getBoundingClientRect().left>=-0.5`);
  await selectLesson(pythonLesson.title,'is-vs-eq');
  await until(`window.__phase8aMonaco.editor.getModels().some(m=>m.uri.toString().includes('is-vs-eq/main.py')) && document.querySelector('.editor-panel textarea')!==null`);
  assert.equal(await evaluate(`window.__phase8aMonaco.editor.getModels().find(m=>m.uri.toString().includes('is-vs-eq/main.py')).getValue()`),pythonFiles['main.py']);
  const comment='# phase8a browser persistence';
  const editedPython=pythonFiles['main.py']+comment;
  await evaluate(`(()=>{const editor=window.__phase8aMonaco.editor.getEditors().find(e=>e.getDomNode()?.closest('.editor-panel'));const model=editor.getModel();const last=model.getLineCount();editor.focus();editor.setPosition({lineNumber:last,column:model.getLineMaxColumn(last)});return true;})()`);
  await call('Input.insertText',{text:comment});
  await until(`window.__phase8aMonaco.editor.getModels().find(m=>m.uri.toString().includes('is-vs-eq/main.py')).getValue()===${JSON.stringify(editedPython)}`);
  await selectLesson(selfLesson.title,'s10-self-join');
  await until(`window.__phase8aMonaco.editor.getModels().some(m=>m.uri.toString().includes('sql.join.20')) && document.querySelector('.sql-footer')?.textContent.includes('сессия активна')`);
  assert.equal(await evaluate(`window.__phase8aMonaco.editor.getModels().find(m=>m.uri.toString().includes('sql.join.20')).getValue()`),tasks[11][2]);
  const savedPython=(await api('/api/lessons/is-vs-eq')).files;
  assert.equal(savedPython['main.py'],editedPython);assert.equal(savedPython['notes.py'],pythonFiles['notes.py']);
  for(const [slug] of tasks)assert.equal((await api('/api/sql/lessons/'+slug)).completed,true);
  assert.equal((await api('/api/course')).summary.xp,0);
  for(const slug of ['s10-data-modification','s11-booking-concurrency']){
    const lesson=await api('/api/lessons/'+slug);
    await selectLesson(lesson.title,slug);
    await until(`document.body.innerText.includes('transaction_lab.cli') && Array.from(document.querySelectorAll('details')).some(d=>d.querySelector('summary')?.textContent==='Показать решение для самопроверки')`);
    const closed=()=>evaluate(`Array.from(document.querySelectorAll('details')).filter(d=>d.querySelector('summary')?.textContent==='Показать решение для самопроверки').map(d=>d.open)`);
    assert.deepEqual(await closed(),[false]);
    await evaluate(`Array.from(document.querySelectorAll('button')).find(b=>b.textContent.includes('Повторение')).click()`);
    assert.deepEqual(await closed(),[false]);
    await evaluate(`Array.from(document.querySelectorAll('button')).find(b=>b.textContent.includes('Обучение')).click()`);
    console.log(JSON.stringify({transactionLesson:slug,localCliDocumented:true,learnReviewAnswerClosed:true}));
  }
  const workerTasks=[['s20-fastapi-backgroundtasks',7],['s20-retry-and-backoff',17],['s20-idempotency',10],['s20-periodic-tasks',14],['s20-delivery-semantics',14]];
  const workerXpBefore=(await api('/api/course')).summary.xp;
  for(const [slug,count] of workerTasks){
    const lesson=await api('/api/lessons/'+slug);
    const reference=await readFile(new URL('../content/stage-20/'+slug+'/solution/main.py',import.meta.url),'utf8');
    const source=reference+"\nif __name__ == '__main__':\n    print('worker-browser-loaded')\n";
    const notes='# independent '+slug+' file\n';
    await api('/api/lessons/'+slug+'/files',{files:{'main.py':lesson.files['main.py'],'notes.py':notes}},'PUT');
    await selectLesson(lesson.title,slug);
    await until(`document.querySelector('.workspace-label')?.textContent.includes(${JSON.stringify(slug)}) && document.querySelector('.editor-panel textarea')!==null && !document.querySelector('.workspace-pane .check-button')?.disabled`);
    await evaluate(`Array.from(document.querySelectorAll('.editor-tabs button')).find(b=>b.textContent.includes('main.py')).click()`);
    await until(`window.__phase8aMonaco.editor.getEditors().some(e=>e.getDomNode()?.closest('.editor-panel')&&e.getModel()?.uri.toString().includes(${JSON.stringify(slug+'/main.py')}))`);
    // Source enters only through native keyboard/text events, never setValue.
    await typePython(source);
    await until(`window.__phase8aMonaco.editor.getModels().find(m=>m.uri.toString().includes(${JSON.stringify(slug+'/main.py')})).getValue()===${JSON.stringify(source)}`);
    await click('.workspace-pane .run-button');
    await until(`document.querySelector('.terminal-result-summary')?.textContent.includes('exit 0') && !document.querySelector('.workspace-pane .run-button').disabled`);
    await click('.workspace-pane .check-button');
    await until(`document.querySelector('.terminal-result-summary .passed')?.textContent.includes('${count} / ${count}') && !document.querySelector('.workspace-pane .check-button').disabled`);
    const saved=await api('/api/lessons/'+slug);
    assert.equal(saved.files['main.py'],source);assert.equal(saved.files['notes.py'],notes);assert.equal(saved.progress.task_completed,true);
    console.log(JSON.stringify({workerLesson:slug,actualMonacoTyping:true,run:true,check:count,twoFilesPreserved:true}));
  }
  assert.equal((await api('/api/course')).summary.xp,workerXpBefore+100);
  await selectLesson(selfLesson.title,'s10-self-join');
  await until(`document.querySelector('.sql-footer')?.textContent.includes('сессия активна')`);
  assert.equal(await evaluate(`window.__phase8aMonaco.editor.getModels().find(m=>m.uri.toString().includes('sql.join.20')).getValue()`),tasks[11][2]);
  await submit(true,`document.querySelector('.sql-check-feedback.passed')?.textContent.includes('6 / 6')`);
  assert.equal((await api('/api/course')).summary.xp,workerXpBefore+100);
  const lastWorker=await api('/api/lessons/s20-delivery-semantics');
  await selectLesson(lastWorker.title,'s20-delivery-semantics');
  await until(`document.querySelector('.workspace-label')?.textContent.includes('s20-delivery-semantics') && document.querySelector('.editor-panel textarea')!==null`);
  assert.equal(await evaluate(`window.__phase8aMonaco.editor.getModels().find(m=>m.uri.toString().includes('s20-delivery-semantics/main.py')).getValue()`),lastWorker.files['main.py']);
  await screenshot('/tmp/pythoria-phase8c-worker-desktop.png');
  await size(390,844,true);
  await until(`document.querySelector('.course-sidebar').getBoundingClientRect().right<=0`);
  assert.equal(await evaluate(`document.documentElement.scrollWidth<=window.innerWidth`),true);
  await screenshot('/tmp/pythoria-phase8c-worker-mobile.png');
  await size(1720,1050);
  await until(`document.querySelector('.course-sidebar').getBoundingClientRect().left>=-0.5`);
  await transactionWalkthrough({api,evaluate,until,selectLesson,call,size,screenshot});
  await selectLesson((await api('/api/lessons/s11-jsonb')).title, 's11-jsonb');
  await stage11Walkthrough();
  await indexWalkthrough({api,evaluate,until,selectLesson,call,size,screenshot});
  await call('Target.closeTarget',{targetId},null);
  console.log(JSON.stringify({browser:'Headless Chrome',allTwentyThree:true,totalChecks:23,newChecks:11,actualMonacoTyping:true,theme:true,monacoShortcuts:true,desktop1720:true,mobile390:true,mobileVisibleRows:2,explorerSelfFK:true,sqlPythonRoundTrip:true,pythonFilesPreserved:true,draftRestoration:true,sqlXpZero:true}));
  }
  }
} finally {
  ws?.close();chrome.kill('SIGTERM');
  if(chrome.pid && chrome.exitCode===null && chrome.signalCode===null)await new Promise(resolve=>chrome.once('exit',resolve));
  await rm(profile,{recursive:true,force:true});
}
