"""Local OpenTelemetry SDK traces with an in-memory ring and a fixed attribute set."""
import asyncio
from collections import deque
from contextlib import contextmanager
from threading import Lock

from opentelemetry.sdk.trace import SpanLimits, TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter, SpanExportResult
from opentelemetry.trace import Status, StatusCode


MODEL_REVISION = "scripted-fact-v1"
PROMPT_REVISION = "bounded-excerpts-v1"
INDEX_REVISION = "pg17-fusion-v1"


class MemoryTrace(SpanExporter):
    def __init__(self):
        self._records = deque(maxlen=512)
        self._lock = Lock()

    def export(self, spans):
        with self._lock:
            self._records.extend(spans)
        return SpanExportResult.SUCCESS

    def get_finished_spans(self):
        with self._lock:
            return tuple(self._records)


class Telemetry:
    def __init__(self):
        self.exporter = MemoryTrace()
        self.provider = TracerProvider(span_limits=SpanLimits(max_attributes=16, max_attribute_length=64),
                                       shutdown_on_exit=False)
        self.provider.add_span_processor(SimpleSpanProcessor(self.exporter))
        self.tracer = self.provider.get_tracer("pythoria.document_rag", "1.0")

    @contextmanager
    def span(self, name, **attrs):
        with self.tracer.start_as_current_span("rag." + name, record_exception=False,
                                               set_status_on_exception=False) as span:
            span.set_attributes(attrs)
            try:
                yield span
            except asyncio.CancelledError:
                fail(span, "cancelled")
                raise
            except Exception:
                fail(span, "operation_failed")
                raise

    def snapshot(self):
        return [
            {
                "name": span.name,
                "trace_id": f"{span.context.trace_id:032x}",
                "span_id": f"{span.context.span_id:016x}",
                "parent": f"{span.parent.span_id:016x}" if span.parent else None,
                "status": span.status.status_code.name,
                "duration_ms": (span.end_time - span.start_time) / 1_000_000,
                "attributes": dict(span.attributes),
            }
            for span in self.exporter.get_finished_spans()
        ]


def fail(span, category):
    span.set_attribute("outcome", category)
    span.set_status(Status(StatusCode.ERROR))
