from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate

class LlmModel:
    def __init__(self, model_path):
        self.model_path = model_path

    def load_llm(
            self,
            callback_manager: CallbackManager = CallbackManager([StreamingStdOutCallbackHandler()]),
            temperature: float = 0.1,
            max_tokens: int = 2000,
            use_gpu: bool = False
            ):
        llm = LlamaCpp(
            model_path=self.model_path,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            callback_manager=callback_manager,
            verbose=True,  # Verbose is required to pass to the callback manager
            #use_gpu=use_gpu  # Enable GPU usage
            #n_gpu_layers = -1  # The number of layers to put on the GPU. The rest will be on the CPU. If you don't know how many layers there are, you can use -1 to move all to GPU.
            #n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
            )
        self.llm = llm

    @staticmethod
    def set_prompt_template(template = None):

        if template is None:
            template = """Question: {question}
                Answer: Let's work this out in a step by step way to be sure we have the right answer."""

        return PromptTemplate.from_template(template)
    
    def generate_api_request(self, prompt):
        # Generar solicitudes para el API (extraer ciudad)
        return self._run_llama(f"Extrae la ciudad de la siguiente pregunta: {prompt}")


    def invoke(self, prompt, template=None):
        try:
            template = self.set_prompt_template(template=None)
            prompt = template.format(question=prompt)
            response = self.llm.invoke(input=prompt)
            return response
        except Exception as e:
            return str(e)