from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate

class LlmModel:
    def __init__(self, model_path):
        self.model_path = model_path

    def load_llm(
            self,
            callback_manager: CallbackManager = CallbackManager([StreamingStdOutCallbackHandler()]),
            temperature: float = 0.3,
            max_tokens: int = 2000
            ):
        llm = LlamaCpp(
            model_path=self.model_path,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            callback_manager=callback_manager,
            verbose=True,  # Verbose is required to pass to the callback manager
            )
        self.llm = llm

    @staticmethod
    def set_prompt_template(self, template):

        if template is None:
            template = """Question: {question}
                Answer: Let's work this out in a step by step way to be sure we have the right answer."""

        return PromptTemplate.from_template(template)

    def invoke_llm(self, prompt, template=None):
        try:
            template = self.set_prompt_template(template=None)
            template.format(question=prompt)
            response = self.llm.invoke(prompt=template)
            return response
        except Exception as e:
            return str(e)