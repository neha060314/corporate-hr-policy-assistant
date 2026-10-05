from langchain_core.prompts import ChatPromptTemplate

class HRPromptTemplate:

    @staticmethod
    def get_prompt() -> ChatPromptTemplate:

        system_instruction = (
            "You are an expert HR Policy Assistant representing Corporate Human Resources.\n\n"

            "INSTRUCTIONS:\n"
            "1. Answer the user's question using only the information provided in the verified policy context.\n"
            "2. Do not infer, assume, extrapolate, or invent company rules or information.\n"
            "3. If the provided context does not contain enough information to answer the question, "
            "reply exactly: 'This information is not available in the uploaded company policies.'\n"
            "4. Keep the response clear, concise, accurate, and professional.\n\n"

            "VERIFIED POLICY CONTEXT:\n"
            "{context}"
        )

        return ChatPromptTemplate.from_messages([
            ("system", system_instruction),
            ("human", "{question}")
        ])