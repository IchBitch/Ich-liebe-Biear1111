import customtkinter as ctk
import os
from PIL import Image

class LogiTalkApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Steam")


        self.attributes("-fullscreen", True)

        self.username = None
        self.users_file = "users.txt"

        if not os.path.exists(self.users_file):
            open(self.users_file, "w").close()

        self.login_screen()

    def login_screen(self):
        self.clear_window()


        img = ctk.CTkImage(light_image=Image.open("image.png"), size=(200, 200))
        logo = ctk.CTkLabel(self, image=img, text="")
        logo.pack(pady=20)


        title = ctk.CTkLabel(self, text="Вхід в Discord", font=("Arial", 28))
        title.pack(pady=40)

        self.login_entry = ctk.CTkEntry(self, placeholder_text="Ім'я користувача", width=300)
        self.login_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Пароль", show="*", width=300)
        self.password_entry.pack(pady=10)

        login_btn = ctk.CTkButton(self, text="Увійти", width=200, command=self.login)
        login_btn.pack(pady=10)

        reg_btn = ctk.CTkButton(self, text="Створити акаунт", width=200, command=self.register_screen)
        reg_btn.pack(pady=10)

    def register_screen(self):
        self.clear_window()

        title = ctk.CTkLabel(self, text="Реєстрація", font=("Arial", 28))
        title.pack(pady=40)

        self.reg_login = ctk.CTkEntry(self, placeholder_text="Новий логін", width=300)
        self.reg_login.pack(pady=10)

        self.reg_pass = ctk.CTkEntry(self, placeholder_text="Новий пароль", show="*", width=300)
        self.reg_pass.pack(pady=10)

        reg_btn = ctk.CTkButton(self, text="Зареєструватися", width=200, command=self.register)
        reg_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="Назад", width=200, command=self.login_screen)
        back_btn.pack(pady=10)

    def register(self):
        username = self.reg_login.get().strip()
        password = self.reg_pass.get().strip()

        if not username or not password:
            self.popup("Заповніть всі поля!")
            return

        if self.user_exists(username):
            self.popup("Користувач з таким ім'ям вже існує!")
            return

        with open(self.users_file, "a") as f:
            f.write(f"{username}:{password}\n")

        self.popup("Реєстрація успішна!")
        self.login_screen()


    def login(self):
        username = self.login_entry.get().strip()
        password = self.password_entry.get().strip()

        if self.validate_user(username, password):
            self.username = username
            self.chat_main_screen()
        else:
            self.popup("Невірний логін або пароль!")

    def user_exists(self, username):
        with open(self.users_file, "r") as f:
            for line in f:
                user, _ = line.strip().split(":")
                if user == username:
                    return True
        return False

    def validate_user(self, username, password):
        with open(self.users_file, "r") as f:
            for line in f:
                user, pas = line.strip().split(":")
                if user == username and pas == password:
                    return True
        return False


    def chat_main_screen(self):
        self.clear_window()


        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)


        left_panel = ctk.CTkFrame(main_frame, width=300)
        left_panel.pack(side="left", fill="y")

        title = ctk.CTkLabel(left_panel, text="Друзі", font=("Arial", 24))
        title.pack(pady=20)

        self.friend_list = ctk.CTkScrollableFrame(left_panel, width=250)
        self.friend_list.pack(fill="y", expand=True)


        users = self.load_users()

        for user in users:
            if user != self.username:
                btn = ctk.CTkButton(
                    self.friend_list,
                    text=user,
                    width=200,
                    command=lambda u=user: self.open_chat(u)
                )
                btn.pack(pady=5)


        self.chat_frame = ctk.CTkFrame(main_frame)
        self.chat_frame.pack(side="right", fill="both", expand=True)

        self.chat_title = ctk.CTkLabel(self.chat_frame, text="Виберіть друга", font=("Arial", 24))
        self.chat_title.pack(pady=20)

        self.chat_box = ctk.CTkTextbox(self.chat_frame, state="disabled", width=900, height=600)
        self.chat_box.pack(pady=20)

        self.msg_entry = ctk.CTkEntry(self.chat_frame, placeholder_text="Введіть повідомлення...", width=800)
        self.msg_entry.pack(pady=10)

        send_btn = ctk.CTkButton(self.chat_frame, text="Надіслати", command=self.send_message)
        send_btn.pack()

        self.current_friend = None


    def load_users(self):
        users = []
        with open(self.users_file, "r") as f:
            for line in f:
                user, _ = line.strip().split(":")
                users.append(user)
        return users


    def open_chat(self, friend):
        self.current_friend = friend
        self.chat_title.configure(text=f"Чат з {friend}")

        self.chat_box.configure(state="normal")
        self.chat_box.delete("1.0", "end")

        chatfile = f"chat_{self.username}_{friend}.txt"
        rev_file = f"chat_{friend}_{self.username}.txt"

        if os.path.exists(chatfile):
            with open(chatfile, "r") as f:
                self.chat_box.insert("end", f.read())
        elif os.path.exists(rev_file):
            with open(rev_file, "r") as f:
                self.chat_box.insert("end", f.read())

        self.chat_box.configure(state="disabled")


    def send_message(self):
        if not self.current_friend:
            self.popup("Спочатку виберіть друга!")
            return

        message = self.msg_entry.get().strip()
        if not message:
            return

        filename = f"chat_{self.username}_{self.current_friend}.txt"

        with open(filename, "a") as f:
            f.write(f"{self.username}: {message}\n")

        self.open_chat(self.current_friend)
        self.msg_entry.delete(0, "end")


    def clear_window(self):
        for w in self.winfo_children():
            w.destroy()

    def popup(self, text):
        top = ctk.CTkToplevel(self)
        top.geometry("300x150")
        top.title("Повідомлення")
        top.grab_set()

        label = ctk.CTkLabel(top, text=text)
        label.pack(pady=20)

        ok_button = ctk.CTkButton(top, text="OK", command=top.destroy)
        ok_button.pack(pady=10)

        top.focus_force()


if __name__ == "__main__":
    app = LogiTalkApp()
    app.mainloop()



