class ContextBuilder:

    def build(self, results):

        context_parts = []

        for index, result in enumerate(
            results,
            start=1,
        ):

            chunk = result["chunk"]

            path = chunk["path"]
            start_line = chunk["start_line"]
            end_line = chunk["end_line"]
            name = chunk["name"]

            source = result["source"]

            part = []

            part.append(
                f"[{index}] {path}:{start_line}-{end_line}"
            )

            part.append(
                f"Name: {name}"
            )

            part.append(
                f"Source: {source}"
            )

            if result["relationship"]:

                part.append(
                    "Relationship: "
                    f"{result['relationship']}"
                )

            if result["direction"]:

                part.append(
                    "Direction: "
                    f"{result['direction']}"
                )

            part.append("")

            part.append(chunk["content"])

            context_parts.append(
                "\n".join(part)
            )

        return "\n\n".join(
            context_parts
        )