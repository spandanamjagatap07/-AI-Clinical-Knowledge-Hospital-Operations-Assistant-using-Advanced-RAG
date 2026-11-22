
import re

from backend.agents.groq_clients import generate_response


def generate_clinical_answer(question, documents):
    """
    Generate a grounded clinical answer using Groq
    and display only validated source citations.
    """

    if not documents:
        return "No relevant hospital documents were found."

    # Prepare retrieved evidence
    context_parts = []
    source_lookup = {}

    for index, document in enumerate(documents, start=1):

        metadata = document.metadata

        source = metadata.get("source", "Unknown")
        department = metadata.get("department", "Unknown")
        document_type = metadata.get("document_type", "Unknown")
        version = metadata.get("version", "Unknown")

        context_parts.append(
            f"""
Evidence {index}:
Source: {source}
Department: {department}
Document Type: {document_type}
Version: {version}

Content:
{document.page_content}
"""
        )

        source_lookup[source] = {
            "source": source,
            "department": department,
            "document_type": document_type,
            "version": version
        }

    context = "\n".join(context_parts)

    # Strict grounding and citation prompt
    prompt = f"""
You are a hospital knowledge assistant.

Answer the user's question using ONLY information
explicitly stated in the supplied hospital documents.

STRICT GROUNDING RULES:

1. Do not use general medical or hospital knowledge.
2. Do not invent actions, responsibilities, systems, or explanations.
3. Do not add assumptions or interpretations.
4. Preserve the original meaning of every procedure step.
5. Follow the original order of numbered workflow steps.
6. Do not combine separate procedures unless the documents
   clearly establish that they belong together.
7. If information is missing, clearly say so.
8. Use simple and professional language.
9. Do not provide medical diagnosis or treatment advice.

CITATION RULES:

1. Every procedure or factual section must have a source citation.
2. Use the exact source filename provided in the evidence.
3. Cite only documents that directly support that section.
4. Never cite a document merely because it was retrieved.
5. Use this exact citation format:

[Source: incident_investigation.txt]

6. Do not invent or modify source filenames.

ANSWER FORMAT:

- Give a short introduction.
- Present the main procedure as numbered steps.
- Include separate supporting procedures only when relevant.
- Put the source citation immediately after each section.
- Keep the answer complete and concise.

USER QUESTION:
{question}

RETRIEVED HOSPITAL DOCUMENTS:
{context}

Generate the answer using the rules above.
"""

    # Generate answer using Groq
    answer = generate_response(prompt)

    # Extract source filenames cited by Groq
    cited_filenames = re.findall(
        r"\[Source:\s*([^\]]+)\]",
        answer,
        flags=re.IGNORECASE
    )

    # Validate citations against retrieved documents
    validated_sources = []
    used_sources = set()

    for filename in cited_filenames:

        filename = filename.strip()

        if filename in source_lookup and filename not in used_sources:

            used_sources.add(filename)
            validated_sources.append(source_lookup[filename])

    # Build final response
    response = []

    response.append("=" * 60)
    response.append("CLINICAL KNOWLEDGE ANSWER")
    response.append("=" * 60)

    response.append(f"\nQUESTION: {question}")

    response.append("\nANSWER")
    response.append("-" * 60)
    response.append(answer)

    response.append("\nSOURCE DOCUMENTS")
    response.append("-" * 60)

    if validated_sources:

        for item in validated_sources:

            response.append(
                f"\nSource: {item['source']}\n"
                f"Department: {item['department']}\n"
                f"Document Type: {item['document_type']}\n"
                f"Version: {item['version']}"
            )

    else:
        response.append(
            "\nNo validated source citations were generated."
        )

    response.append("\n" + "=" * 60)

    return "\n".join(response)
