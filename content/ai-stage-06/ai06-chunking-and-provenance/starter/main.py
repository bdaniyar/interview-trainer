def chunk_text(document_id, version, text, size, overlap):
    return ()


if __name__ == "__main__":
    for chunk in chunk_text("guide", 1, "# Ауа\nТаза ауа", 7, 2):
        print(chunk.page, chunk.section, (chunk.start, chunk.end), repr(chunk.text))
