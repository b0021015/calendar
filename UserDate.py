import tkinter as tk
import tkinter.ttk as ttk
import datetime as da
import calendar as ca
import pymysql.cursors
import YicDiary

class Login:
    def __init__(self, master):
        #コンストラクタ
        #master:ログイン画面を配置するウィジェット
        #body:アプリ本体のクラスのインスタンス

        #root.title('ログイン画面')
        #root.geometry('300x300')
        #root.resizable(0, 0)
        #root.grid_columnconfigure((0, 1), weight=1)
        #master.withdraw()
        
        self.master = master
        self.master.title('ログイン画面')

        #ログイン関連のウィジェットを管理するリスト
        self.widgets = []

        #ログイン用のフラグ変数
        self.flag = True
        #ログイン失敗のカウント用変数
        self.MissCount = 0

        #ログイン用の表示
        self.showlogin = "*"

        #登録用用の表示
        self.showregis = "*"


        #ログイン画面のウィジェット作成
        self.create_widgets()

        #登録時のフラグ変数
        self.regflag = True


    #ウィジェットの作成・配置
    def create_widgets(self):
        #表示中のウィジェットを一旦削除
        for widget in self.widgets:
            widget.destroy()
        
        '''
        def callback(event):
            #テキスト取得
            #str(event.widget["text"])
            self.show = ""
            #self.create_widgets()
            #self.pass_entry.insert(tk.END. str(text))
            self.pass_label = tk.Entry(self.master, show = "")
            self.pass_label.grid(row = 1, column = 1)
            self.pass_label.tkraise()

        def callback2(event):
            self.show = "*"
            self.pass_label = tk.Entry(self.master, show = "*")
            self.pass_label.grid(row = 1, column = 1)
            self.pass_label.tkraise()
        '''

        self.name_label = tk.Label(self.master, text="ユーザー名")
        self.name_label.grid(row=0, column=0)

        self.widgets.append(self.name_label)

        self.name_entry = tk.Entry(self.master)
        self.name_entry.grid(row = 0, column = 1)

        self.widgets.append(self.name_entry)

        #パスワード入力用のウィジェット
        self.pass_label = tk.Label(self.master, text="パスワード")
        self.pass_label.grid(row = 1, column = 0)

        self.widgets.append(self.pass_label)
        
        self.pass_entry = tk.Entry(self.master, show = self.showlogin)
        self.pass_entry.grid(row = 1, column = 1)

        self.widgets.append(self.pass_entry)

        #ボタンを押した時に変更するパターン
        self.pass_button = tk.Button(self.master, text = "パスワードの表示切り替え", command = self.loginPassSwich)
        self.pass_button.grid(row = 1, column = 3)

        self.widgets.append(self.pass_button)

        #ボタンを押している間表示するパターン
        '''
        self.pass_button = tk.Button(self.master, text = "パスワードの表示切り替え")
        self.pass_button.grid(row = 1, column = 3)
        self.pass_button.bind("<Button-1>", callback)
        self.pass_button.bind("<ButtonRelease>", callback2, '+')
        self.widgets.append(self.pass_button)
        '''

        #ログインボタン
        self.login_button = tk.Button(self.master, text = "ログイン", command = self.login)
        self.login_button.grid(row = 2, column = 1, columnspan = 1)

        self.widgets.append(self.login_button)

        #登録ボタン
        self.register_button = tk.Button(self.master, text = "登録画面", command = self.register)
        self.register_button.grid(row = 3, column = 1, columnspan = 2)

        self.widgets.append(self.register_button)

        if (self.flag == False):
            self.MissMassage_label = tk.Label(self.master, text = "ユーザー名かパスワードが間違ってます")
            self.MissMassage_label.grid(row = 5, column = 0, columnspan = 3)

            self.widgets.append(self.MissMassage_label)
        #ウィジェットを全て中央寄せにする
        self.master.grid_anchor(tk.CENTER)


    #押した時に表示を変更するパターン
    def loginPassSwich(self):
        if self.showlogin == "*":
            self.showlogin = ""
        else:
            self.showlogin = "*"
        text_entry = self.pass_entry.get()
        text_name = self.name_entry.get()
        #print(text)
        self.create_widgets()
        self.name_entry.insert(tk.END, text_name)
        self.pass_entry.insert(tk.END, text_entry)


    def login(self):
        
        # 入力された情報をEntryウィジェットから取得
        username = self.name_entry.get()
        password = self.pass_entry.get()
        self.flag = False
        #
        connection = pymysql.connect(host = '127.0.0.1',
                                    user = 'root',
                                    password = '',
                                    db = 'apr01',
                                    charset = 'utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

        try:
            #トランザクション開始
            connection.begin()
            
            with connection.cursor() as cursor:

                cursor = connection.cursor()

                #後でメールアドレスに変更しておくこと
                #その後このコメントを削除する
                #こちらは登録されているかどうか
                sql = "SELECT user_name FROM user_table WHERE '{}' = user_name".format(username)
                cursor.execute(sql)
                resultUser = cursor.fetchone()
                if resultUser is not None:
                    resultUser = resultUser['user_name']

                #こちらは一致しているかどうか
                sql = "SELECT access_id FROM access_table WHERE '{}' = password".format(password)
                cursor.execute(sql)
                resultPath = cursor.fetchone()
                if resultPath is not None:
                    resultPath = resultPath['access_id']

                #ユーザーの情報
                sql = "SELECT * FROM user_table WHERE '{}' = user_name AND '{}' = access_id".format(resultUser, resultPath)
                cursor.execute(sql)
                result = cursor.fetchone()

            connection.commit()


            #登録されているユーザー名・パスワード
            if result is not None:
                    # ログインユーザー名を設定
                    self.login_date = result
                    #self.success()
                    self.flag = True
            else:
                self.MissCount += 1

        except Exception as e:
            print('error:', e)
            connection.rollback()
        finally:
            connection.close()

        if (self.flag):
            self.success()
        elif self.MissCount % 3 == 0:
            self.MissFinish()
        else:
            #create_widgets()で消した時、入力された名前とパスワードも消える
            self.create_widgets()

    def success(self):
        #ログイン成功時の処理を実行する

        #表示中のウィジェットを削除
        for widget in self.widgets:
            widget.destroy()

        #"ログインに成功しました"メッセージを表示
        self.message = tk.Label(self.master, text = "ログインに成功しました", font = ("", 20))
        self.message.place(x = self.master.winfo_width() // 2, y = self.master.winfo_height() // 2, anchor = tk.CENTER)
        #self.message.place(x = 0, y = 0, anchor = tk.CENTER)

        # 少しディレイを入れてredisplayを実行
        self.master.after(1000, self.main_start)


    def main_start(self):
        #アプリ本体を起動する
        ##表示中のウィジェットを削除
        #for widget in self.widgets:
        #    widget.destroy()

        #"ログインに成功しました"のメッセージを削除
        self.message.destroy()
        #print(self.login_date)

        #アプリ本体を起動
        self.master.destroy()
        root = tk.Tk()
        YicDiary.YicDiary(root, self.login_date)

    def MissFinish(self):
        #ログインに一定数失敗した時の処理
        
        #表示中のウィジェットを削除
        for widget in self.widgets:
            widget.destroy()

        #"ログインに失敗しました"メッセージを表示
        self.message = tk.Label(self.master, text = "ログインに一定数失敗しました", font = ("", 15))
        self.message.place(x = 0, y = 0)
        self.widgets.append(self.message)

        #self.message2 = tk.Label(self.master, text = "{}秒後にログイン画面が開きます".format(self.MissCount * 10), font = ("", 15))
        self.message2 = tk.Label(self.master, text = "{}秒後にログイン画面が開きます". format(self.MissCount), font = ("", 15))
        self.message2.place(x = 0, y = 50)
        self.widgets.append(self.message2)

        self.master.grid_anchor(tk.CENTER)
        #print(self.MissCount)

        # 少しディレイを入れて画面を削除
        #self.master.after(5000, self.master.destroy)

        # ミスをした数×10秒後にログイン画面を表示

        #ミスをした数秒後にログイン画面を表示
        self.master.after(self.MissCount * 1000, self.create_widgets)
       
        



    #ユーザー名とパスワードの登録
    #後で変更する(理由:同じ画面では登録がしにくいので、別の画面で登録するようにする)
    #よって後に登録専用の画面を用意する。
    def register(self):
        #表示中のウィジェットを一旦削除
        for widget in self.widgets:
            widget.destroy()

        self.name_label = tk.Label(self.master, text = "登録するユーザー名")
        self.name_label.grid(row = 0, column = 0)
        self.widgets.append(self.name_label)

        self.name_entry = tk.Entry(self.master)
        self.name_entry.grid(row = 0, column = 1)
        self.widgets.append(self.name_entry)

        self.pass_label = tk.Label(self.master, text = "登録するパスワード")
        self.pass_label.grid(row = 1, column = 0)
        self.widgets.append(self.pass_label)

        self.pass_entry = tk.Entry(self.master, show = self.showregis)
        self.pass_entry.grid(row = 1, column = 1)
        self.widgets.append(self.pass_entry)

        #パスワードの確認用
        self.passconfir_label = tk.Label(self.master, text = "パスワードの確認")
        self.passconfir_label.grid(row = 2, column = 0)
        self.widgets.append(self.passconfir_label)

        self.passconfir_entry = tk.Entry(self.master, show = self.showregis)
        self.passconfir_entry.grid(row = 2, column = 1)
        self.widgets.append(self.passconfir_entry)

        #ボタンを押した時にパスワードの表示を変更する
        self.pass_button = tk.Button(self.master, text = "パスワードの表示切り替え", command = self.registerPassSwich)
        self.pass_button.grid(row = 2, column = 2)

        self.widgets.append(self.pass_button)

        #ログイン画面へ
        self.login_button = tk.Button(self.master, text = "ログイン画面", command = self.create_widgets)
        self.login_button.grid(row = 4, column = 0, columnspan = 2)
        self.widgets.append(self.login_button)


        #登録ボタン
        self.register_button = tk.Button(self.master, text = "登録", command = self.registerCheck)
        self.register_button.grid(row = 3, column = 0, columnspan = 2)
        self.widgets.append(self.register_button)

        if (self.regflag == False):
            self.MissMassage_label = tk.Label(self.master, text = "登録ができませんでした")
            self.MissMassage_label.grid(row = 5, column = 0, columnspan = 3)

            self.widgets.append(self.MissMassage_label)


        #ウィジェットを全て中央寄せにする
        self.master.grid_anchor(tk.CENTER)

    #登録時のパスワード用の切り替え
    def registerPassSwich(self):
        if self.showregis == "*":
            self.showregis = ""
        else:
            self.showregis = "*"
        text_entry = self.pass_entry.get()
        text_passconfir = self.passconfir_entry.get()
        text_name = self.name_entry.get()
        #print(text)
        self.register()
        self.name_entry.insert(tk.END, text_name)
        self.pass_entry.insert(tk.END, text_entry)
        self.passconfir_entry.insert(tk.END, text_passconfir)


    def registerCheck(self):

        # 入力された情報をEntryウィジェットから取得
        username = self.name_entry.get()
        password = self.pass_entry.get()
        passconfir = self.passconfir_entry.get()

        #取得した情報をテーブルに記載
        connection = pymysql.connect(host = '127.0.0.1',
                                    user = 'root',
                                    password = '',
                                    db = 'apr01',
                                    charset = 'utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        try:
            #トランザクション開始
            connection.begin()
            
            with connection.cursor() as cursor:

                cursor = connection.cursor()


                # 'を\'にできるようにしておくこと
                #'を入力する場合エラーが起きる
                #スペースにも気を付ける
                sql = "SELECT user_name FROM user_table WHERE '{}' = user_name".format(username)
                cursor.execute(sql)
                resultUser = cursor.fetchone()
                

                sql = "SELECT access_id FROM access_table WHERE '{}' = password".format(password)
                cursor.execute(sql)
                resultPath = cursor.fetchone()
                #print(resultPath)
                #print(resultUser)
                Spaceusername = username.split()
                Spacepassword = password.split()
                #print(username)
                #print(password)
                #print(passconfir)


                if resultPath is None and resultUser is None and password == passconfir and Spaceusername != [] and Spacepassword != []:
                    sql = "INSERT INTO access_table(password) VALUES ('{}')".format(password)
                    cursor.execute(sql)
                    sql = "SELECT access_id FROM access_table WHERE '{}' = password".format(password)
                    cursor.execute(sql)
                    access_id = cursor.fetchone()
                    access_id = access_id['access_id']
                    #print(access_id)
                    sql = "INSERT INTO user_table(user_name, access_id) VALUES('{}', {})".format(username, access_id)
                    cursor.execute(sql)

                    sql = "SELECT * FROM user_table WHERE '{}' = user_name AND '{}' = access_id".format(username, access_id)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    self.regflag = True
                else:
                    self.regflag = False

                    

            connection.commit()

        except Exception as e:
            print('error:', e)
            connection.rollback()
        finally:
            connection.close()
            if (self.regflag):
                self.login_date = result
                self.Rsuccess()
            else:
                self.register()

    def Rsuccess(self):
        #登録成功時の処理を実行する

        #表示中のウィジェットを削除
        for widget in self.widgets:
            widget.destroy()

        #"ログインに成功しました"メッセージを表示
        self.message = tk.Label(self.master, text = "登録に成功しました\nログインします", font = ("", 20))
        self.message.place(x = self.master.winfo_width() // 2, y = self.master.winfo_height() // 2, anchor = tk.CENTER)
        #self.message.place(x = 0, y = 0, anchor = tk.CENTER)

        # 少しディレイを入れてredisplayを実行
        self.master.after(1000, self.main_start)







        
def Main():
    root = tk.Tk()
    root.geometry("500x300")
    Login(root)
    #root.Login()
    root.mainloop()

if __name__ == '__main__':
    Main()
