def create_chunks(structured_data, max_words=100):

    chunks = []

    current_chunk = None
    current_word_count = 0

    for item in structured_data:

        words = item["content"].split()
        word_count = len(words)

        # Create the first chunk
        if current_chunk is None:

            current_chunk = {
                "unit": item["unit"],
                "topic": item["topic"],
                "section": item["section"],
                "content": ""
            }

            current_word_count = 0

        # Check whether metadata is the same
        same_section = (
            current_chunk["unit"] == item["unit"]
            and current_chunk["topic"] == item["topic"]
            and current_chunk["section"] == item["section"]
        )

        # If section changed
        if not same_section:

            if current_chunk["content"]:
                chunks.append(current_chunk)

            current_chunk = {
                "unit": item["unit"],
                "topic": item["topic"],
                "section": item["section"],
                "content": ""
            }

            current_word_count = 0

        # Content fits inside current chunk
        if current_word_count + word_count <= max_words:

            if current_chunk["content"]:
                current_chunk["content"] += " "

            current_chunk["content"] += item["content"]
            current_word_count += word_count

        # Content does not fit
        else:

            # Save current chunk
            if current_chunk["content"]:
                chunks.append(current_chunk)

            # If one paragraph is itself larger than max_words
            if word_count > max_words:

                for i in range(0, word_count, max_words):

                    part_words = words[i:i + max_words]

                    chunks.append({
                        "unit": item["unit"],
                        "topic": item["topic"],
                        "section": item["section"],
                        "content": " ".join(part_words)
                    })

                current_chunk = None
                current_word_count = 0

            else:

                current_chunk = {
                    "unit": item["unit"],
                    "topic": item["topic"],
                    "section": item["section"],
                    "content": item["content"]
                }

                current_word_count = word_count

    # Save final chunk
    if current_chunk is not None and current_chunk["content"]:

        chunks.append(current_chunk)

    return chunks
