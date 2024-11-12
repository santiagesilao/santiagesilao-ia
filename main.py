import streamlit as st #importamos la libreria
from groq import Groq #? NUEVA IMPORTACION

#Le Damos un titulo a la web
st.set_page_config(page_title="Mi chat de IA", page_icon="👩🏿‍🦲")

#Titulo de la pagina
st.title("Mi primera aplicacion con Streamlit")

#Ingreso de datos
nombre = st.text_input("¿Cual es tu nombre?")

#Crear un boton con funcionalidad
if st.button("Saludar") :
    st.write(f"Hola, {nombre}! Gracias por entrar a la pagina web")

MODELO = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

#nos conecta a la API, crear un usuario
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"] #obteniendo la clave en nuestro archivo
    return Groq(api_key = clave_secreta) #crea al usuario

#cliente = usuario de groq | modelo es la IA seleccionada | mensaje del usuario
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user", "content": mensajeDeEntrada}],
        stream = False 
    )
def inicializar_estado(): #-> simula un historial de mensajes
    #Si "mensajes" no esta en st.session_state 
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [] #memoria de mensajes

def actualizar_historial(rol, contenido, avatar):
    #el metodo append() agrega un elemento a la lista
    st.session_state.mensajes.append(
         {"role": rol, "content": contenido, "avatar": avatar}
    )
def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar= mensaje["avatar"]) : st.markdown(mensaje["content"])
#contenedor del chat
def area_chat():
    contenedorDelChat = st.container(height= 400, border= True)
    #agrupamos los mensajes en el area del chat
    with contenedorDelChat : mostrar_historial()
#? CREANDO FUNCION -> con diseño de la pagina 
def configurar_pagina():
    st.title("Mi chat de IA")
    st.sidebar.title("Configuración")
    seleccion = st.sidebar.selectbox(
        "Elegí un modelo", #Titulo
        MODELO, #tiene que estar en una lista
        index = 0 #datoDefecto
    )   

    return seleccion #Devuelve un dato
    #invocacion de funciones
modelo = configurar_pagina() #llamamos a la funcion
clienteUsuario = crear_usuario_groq()
inicializar_estado() #llama a la funcion historial
area_chat()#? creamos el sector para ver los mensajes
mensaje =  st.chat_input("Escribí tu mensaje: ")
#st.write(f"usuario: {mensaje}")

#verificar si el mensaje tiene contenido
if mensaje:
    actualizar_historial("user", mensaje, "👩🏿‍🦲")
    chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
    actualizar_historial("assistant", chat_completo, "🤖")
    st.rerun()
    #print(mensaje)









def generar_respuestas(chat_completo):
    respuesta_completa = "" #texto vacio
    for frase in chat_completo:
        if frase.choice[0].delta.content: 
            respuesta_completa += frase.choice[0].delta.content
            yield frase.choices[0].delta.content
    
    return respuesta_completa


def main(): #funcion principal
    #invocacion  de funciones
    modelo = configurar_pagina() #llamamos a la funcion
    clienteUsuario = crear_usuario_groq() #crea el usuario para usar la api
    inicializar_estado()#crea el historial vacio de mensaje
    area_chat()#? creamos el sector para ver los mensajes
    mensaje = st.chat_input("Escribí tu mensaje...")

    #verificamos si el mensaje tiene contenido
    if mensaje:
        actualizar_historial("user", mensaje, "👩🏿‍🦲") #visualizamos el msg del usuario
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuestas(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
                st.rerun()

#indicamos que nuestra funcion principal es main()
if __name__ == "__main__":
    main()


