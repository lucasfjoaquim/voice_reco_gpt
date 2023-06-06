import tkinter
import speech_recognition as sr
import openai
import pyttsx3

openai.api_key = "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"

# Cria um reconhecedor
engine = pyttsx3.init()
r = sr.Recognizer()


def microfone():
    # Captura o áudio do microfone
    with sr.Microphone() as source:
        print("Fale algo:")
        audio = r.listen(source)

    try:
        # Usa o reconhecedor do Google para transcrever o áudio
        frase = r.recognize_google(audio, language='pt-BR')
        print(f"voce disse: {frase}")
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio")
    except sr.RequestError as e:
        print("Erro ao solicitar resultados do serviço do Google Speech Recognition; {0}".format(e))

    perguntar_para_gpt(frase)


def gerar_resposta(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,
        temperature=0.5
    )
    return [response.choices[0].message.content, response.usage]


mensagens = [{"role": "system", "content": "Você é um assistente gente boa."}]


def perguntar_para_gpt(pergunta):
    # pergunta
    question = pergunta

    mensagens.append({"role": "user", "content": str(question)})

    answer = gerar_resposta(mensagens)
    print("ChatGPT:", answer[0])
    mensagens.append({"role": "assistant", "content": answer[0]})
    engine.say(answer[0])
    engine.runAndWait()

    debugar = False
    if debugar:
        print("Mensagens", mensagens, type(mensagens))


def treinar_gpt(pergunta):
    # pergunta
    question = pergunta

    mensagens.append({"role": "user", "content": str(question)})

    answer = gerar_resposta(mensagens)
    mensagens.append({"role": "assistant", "content": answer[0]})

    debugar = False
    if debugar:
        print("Mensagens", mensagens, type(mensagens))


treinar_gpt(
    "voce deve comportar como um assistente virtual de uma firma de advocacioa, voce deve deve saber responder apenas perguntar do ramo, em caso de uma pergunta fora do ramo voce deve responder: não sei te informar, sou apenas um assistente de advocacia, e deve usar como referencia o codigo penal brasileiro e casos judiciais importantes, suas respostas devem ter no maximo 300 caracteres")

# Cria a janela
janela = tkinter.Tk()

# Define o tamanho da janela e a cor de fundo
janela.geometry("400x300")
janela.configure(bg="#333333")

# Define um estilo para o botão

# Cria o botão com o estilo personalizado
botao = tkinter.Button(janela, text="Começe a falar", command=microfone, bg='#003366', font=('Helvetica', 12))
botao.pack(pady=20)
botao.configure(width=20)


# Inicia o loop principal da interface
janela.mainloop()
