# 📌 Agent Registration Guide

## 🖥️ Registration on Linux

To register the agent on Linux, run the following command with root permissions:

```bash
cmk-update-agent register -v
```

### 🔹 Steps:
1. Enter the hostname as it is registered in Checkmk.
2. Enter the registration user: `cmkadmin`.
3. Enter the password.

### ✅ Verification of Registration
To check if the registration was successful, there are two options:

- **From the host:** Run the following command:
  
  ```bash
  cmk-update-agent -v
  ```
  
  If the registration is successful, it should display a result where the `Target Hash` matches the agent created in Checkmk.

---

## 🖥️ Registration on Windows

To register the agent on Windows, open the command console with administrator privileges and run:

```cmd
"C:\Program Files (x86)\checkmk\service\check_mk_agent.exe" updater register
```

### 🔹 Steps:
1. Enter the hostname.
2. Enter the registration user: `cmkadmin`.
3. Enter the password.

The process is the same as in Linux.

---

📌 **Note:** Make sure you have the appropriate permissions before executing the commands.

---

# 📌 Guía de Registro de Agentes

## 🖥️ Registro en Linux

Para registrar el agente en Linux, ejecuta el siguiente comando con permisos de root:

```bash
cmk-update-agent register -v
```

### 🔹 Pasos:
1. Introducir el nombre del host, tal como está registrado en Checkmk.
2. Ingresar el usuario de registro: `cmkadmin`.
3. Introducir la contraseña.

### ✅ Verificación del Registro
Para comprobar si el registro se realizó correctamente, hay dos opciones:

- **Desde el host:** Ejecuta el siguiente comando:
  
  ```bash
  cmk-update-agent -v
  ```
  
  Si el registro es exitoso, debería mostrar un resultado donde el `Target Hash` coincida con el del agente creado en Checkmk.

---

## 🖥️ Registro en Windows

Para registrar el agente en Windows, abre la consola de comandos con permisos de administrador y ejecuta:

```cmd
"C:\Program Files (x86)\checkmk\service\check_mk_agent.exe" updater register
```

### 🔹 Pasos:
1. Introducir el hostname.
2. Ingresar el usuario de registro: `cmkadmin`.
3. Introducir la contraseña.

El proceso es el mismo que en Linux.

---

📌 **Nota:** Asegúrate de tener los permisos adecuados antes de ejecutar los comandos.
