import tkinter as tk
import tkinter.ttk as ttk
import datetime as da
import calendar as ca
import pymysql.cursors
import UserDate

WEEK = ['日', '月', '火', '水', '木', '金', '土']
WEEK_COLOUR = ['red', 'black', 'black', 'black','black', 'black', 'blue']
actions = ('学校','試験', '課題', '行事', '就活', 'アルバイト','旅行')

class YicDiary:
  def __init__(self, root, UserDate=None):
    #self.User = self.login_date
    #print(self.User)
    self.User = None
    if UserDate is not None:
      self.User = UserDate
    print(UserDate)
    root.title('予定管理アプリ')
    root.geometry('520x280')
    root.resizable(0, 0)
    root.grid_columnconfigure((0, 1), weight=1)
    self.sub_win = None

    #'''
    #geometry('+'+str(w)+'+0'): 位置の指定
    #winfo_screenwidth()        モニターの横幅取得
    #winfo_screenheight()       モニターの縦幅取得
    #w = root.winfo_screenwidth()
    #w1 = root.winfo_screenwidth()  #横
    #w2 = root.winfo_screenheight() #縦
    #下記の場合モニターの右上に表示する
    #w = w - 520
    #w2 = w2 // 2
    #root.geometry('+'+str(w)+"+0")
    #a = root.geometry()
    #print(root.geometry())
    '''
    x = root.winfo_screenwidth() // 2
    y = root.winfo_screenheight() // 2
    root.geometry(f'+{x}+{y}')
    '''


    self.year  = da.date.today().year
    self.mon = da.date.today().month
    self.today = da.date.today().day

    #self.schedules = None
    #self.user_win = None
    #self.user_id, self.user_name = self.user_date()

    self.userCombo = None
    self.userbutton = None
    

    self.title = None
    # 左側のカレンダー部分
    leftFrame = tk.Frame(root)
    leftFrame.grid(row=0, column=0)
    self.leftBuild(leftFrame)

    # 右側の予定管理部分
    rightFrame = tk.Frame(root)
    rightFrame.grid(row=0, column=1)
    self.rightBuild(rightFrame)

    self.userlist()
  #-----------------------------------------------------------------
  # アプリの左側の領域を作成する
  #
  # leftFrame: 左側のフレーム
  def leftBuild(self, leftFrame):
    self.viewLabel = tk.Label(leftFrame, font=('', 10))
    beforButton = tk.Button(leftFrame, text='＜', font=('', 10), command=lambda:self.disp(-1))
    nextButton = tk.Button(leftFrame, text='＞', font=('', 10), command=lambda:self.disp(1))

    self.viewLabel.grid(row=0, column=1, pady=10, padx=10)
    beforButton.grid(row=0, column=0, pady=10, padx=10)
    nextButton.grid(row=0, column=2, pady=10, padx=10)

    self.calendar = tk.Frame(leftFrame)
    self.calendar.grid(row=1, column=0, columnspan=3)
    #self.disp(0)

    self.ComboUser = tk.Frame(leftFrame)
    self.ComboUser.grid(row = 5, column = 0)
    self.disp(0)



  #-----------------------------------------------------------------
  # アプリの右側の領域を作成する
  #
  # rightFrame: 右側のフレーム
  def rightBuild(self, rightFrame):
    r1_frame = tk.Frame(rightFrame)
    r1_frame.grid(row=0, column=0, pady=10)

    temp = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)
    self.title = tk.Label(r1_frame, text=temp, font=('', 12))
    self.title.grid(row=0, column=0, padx=20)
    if self.User is not None:
      button = tk.Button(rightFrame, text='追加', command=lambda:self.add())
      button.grid(row=0, column=1)

    self.r2_frame = tk.Frame(rightFrame)
    self.r2_frame.grid(row=1, column=0)

    self.schedule()

  #-----------------------------------------------------------------
  # アプリの右側の領域に予定を表示する
  #
  def schedule(self):
    # ウィジットを廃棄 
    for widget in self.r2_frame.winfo_children():
      widget.destroy()

    # データベースに予定の問い合わせを行う

    temp = ''
    connection = pymysql.connect(host = '127.0.0.1',
                                 user = 'root',
                                 password = '',
                                 db = 'apr01',
                                 charset = 'utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        # トランザクション開始
        connection.begin()

        with connection.cursor() as cursor:

            cursor = connection.cursor()
            #sql = "select memo from schedule where days = '{}-{}-{}'".format(self.year, self.mon, self.today)
            #全員の場合
            sql = "select memo, kinds from schedule inner join kinds_table on schedule.kinds_id = kinds_table.kinds_id where days = '{}-{}-{}'".format(self.year, self.mon, self.today)

            #誰かの場合
            #sql = "select memo, kinds from schedule inner join kinds_table on schedule.kinds_id = kinds_table.kinds_id inner join user_table on schedule.user_id = user_table.user_id where days = '{}-{}-{}', user_name = '{}'".format(self.year, self.mon, self.today)
            print(sql)

            print(cursor.execute(sql))

            results = cursor.fetchall()

            for i, row in enumerate(results):
                temp += ("・{}: {}\n".format(row["kinds"], row["memo"]))
                #temp += (row["memo"])
        print(temp)

        connection.commit()

    except Exception as e:
        print('error:', e)
        connection.rollback()
    finally:
        connection.close()

    temp = temp[:-1]
    test = tk.Label(self.r2_frame, text=temp, font=('', 12))
    test.grid(row=0, column=0, padx=20)

  #-----------------------------------------------------------------
  #ユーザー表示のコンボボックス作成
  def userlist(self):
    if self.userCombo is not None:
     # for widget in self.userCombo:
     #   widget.destroy()
      self.userCombo.destroy()
    if self.userbutton is not None:
      self.userbutton.destroy()

    '''
      sb2_frame = tk.Frame(self.sub_win)
      sb2_frame.grid(row=1, column=0)
      label_1 = tk.Label(sb2_frame, text='種別 : 　', font=('', 10))
      label_1.grid(row=0, column=0, sticky=tk.W)
      self.combo = ttk.Combobox(sb2_frame, state='readonly', values=actions)
      self.combo.current(0)
      self.combo.grid(row=0, column=1)
    '''

    self.schedulePut = []
    connection = pymysql.connect(host = '127.0.0.1',
                                 user = 'root',
                                 password = '',
                                 db = 'apr01',
                                 charset = 'utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        # トランザクション開始
        connection.begin()
        with connection.cursor() as cursor:

            cursor = connection.cursor()
            sql = "select user_name, user_table.user_id from schedule inner join user_table on schedule.user_id = user_table.user_id where days = '{}-{}-{}'".format(self.year, self.mon, self.today)
            cursor.execute(sql)
            results = cursor.fetchall()
            #print(results)
            if len(results) != 0:
              self.schedulePut.append('全員')
              for i, row in enumerate(results):
                  print(i, row)
                  self.schedulePut.append(row['user_name'])
                    
              print(self.schedulePut)
              print(self.schedulePut[0])
              v = tk.StringVar()
            #コンボボックス
            #self.userCombo = ttk.Combobox(self.ComboUser, textvariable = 'readonly', values = self.schedulePut, width=10)
            self.userCombo = ttk.Combobox(self.ComboUser, state = 'readonly', values = self.schedulePut, width=10)
            #コンボボックスの初期配置
            #userCombo.set(self.schedulePut[0])
            self.userCombo.current(0)
            #userCombo.bind('<<ComboboxSelected>>', command = self.schedule())
            self.userCombo.grid(row = 0, column = 1)
        connection.commit()
    
    except Exception as e:
      print('error:', e)
      connection.rollback()
    finally:
      connection.close()
    self.userbutton = ttk.Button(self.ComboUser, text = 'OK', command = lambda:self.schedule())
    self.userbutton.grid(row = 1, column = 1)


  #-----------------------------------------------------------------
  # カレンダーを表示する
  #
  # argv: -1 = 前月
  #        0 = 今月（起動時のみ）
  #        1 = 次月
  def disp(self, argv):
    self.mon = self.mon + argv
    if self.mon < 1:
      self.mon, self.year = 12, self.year - 1
    elif self.mon > 12:
      self.mon, self.year = 1, self.year + 1

    self.viewLabel['text'] = '{}年{}月'.format(self.year, self.mon)

    cal = ca.Calendar(firstweekday=6)
    cal = cal.monthdayscalendar(self.year, self.mon)

    # ウィジットを廃棄
    for widget in self.calendar.winfo_children():
      widget.destroy()

    # 見出し行
    r = 0
    for i, x in enumerate(WEEK):
      label_day = tk.Label(self.calendar, text=x, font=('', 10), width=3, fg=WEEK_COLOUR[i])
      label_day.grid(row=r, column=i, pady=1)

    # カレンダー本体
    r = 1
    for week in cal:
      for i, day in enumerate(week):
        if day == 0: day = ' ' 
        label_day = tk.Label(self.calendar, text=day, font=('', 10), fg=WEEK_COLOUR[i], borderwidth=1)
        if (da.date.today().year, da.date.today().month, da.date.today().day) == (self.year, self.mon, day):
          label_day['relief'] = 'solid'
        label_day.bind('<Button-1>', self.click)
        label_day.grid(row=r, column=i, padx=2, pady=1)
      r = r + 1

    # 画面右側の表示を変更
    if self.title is not None:
      self.today = 1
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, self.today)

      text = tk.Label(self.r2_frame, font=('', 12))
      #text = tk.Label(self.r2_frame, text=3, font=('', 12))
      text.grid(row=0, column=0, padx=10)


  #-----------------------------------------------------------------
  # 予定を追加したときに呼び出されるメソッド
  #
  def add(self):
    if self.sub_win == None or not self.sub_win.winfo_exists():
      self.sub_win = tk.Toplevel()
      self.sub_win.geometry("300x300")
      self.sub_win.resizable(0, 0)


      # ラベル
      sb1_frame = tk.Frame(self.sub_win)
      sb1_frame.grid(row=0, column=0)
      temp = '{}年{}月{}日　追加する予定'.format(self.year, self.mon, self.today)
      title = tk.Label(sb1_frame, text=temp, font=('', 12))
      title.grid(row=0, column=0)

      # 予定種別（コンボボックス）
      sb2_frame = tk.Frame(self.sub_win)
      sb2_frame.grid(row=1, column=0)
      label_1 = tk.Label(sb2_frame, text='種別 : 　', font=('', 10))
      label_1.grid(row=0, column=0, sticky=tk.W)
      self.combo = ttk.Combobox(sb2_frame, state='readonly', values=actions)
      self.combo.current(0)
      self.combo.grid(row=0, column=1)

      # テキストエリア（垂直スクロール付）
      sb3_frame = tk.Frame(self.sub_win)
      sb3_frame.grid(row=2, column=0)
      self.text = tk.Text(sb3_frame, width=40, height=15)
      self.text.grid(row=0, column=0)
      scroll_v = tk.Scrollbar(sb3_frame, orient=tk.VERTICAL, command=self.text.yview)
      scroll_v.grid(row=0, column=1, sticky=tk.N+tk.S)
      self.text["yscrollcommand"] = scroll_v.set

      # 保存ボタン
      sb4_frame = tk.Frame(self.sub_win)
      sb4_frame.grid(row=3, column=0, sticky=tk.NE)
      button = tk.Button(sb4_frame, text='保存', command=lambda:self.done())
      button.pack(padx=10, pady=10)
    elif self.sub_win != None and self.sub_win.winfo_exists():
      self.sub_win.lift()

  #-----------------------------------------------------------------
  # 予定追加ウィンドウで「保存」を押したときに呼び出されるメソッド
  #
  def done(self):
    # 日付
    days = '{}-{}-{}'.format(self.year, self.mon, self.today)

    # 種別
    kinds = self.combo.get()

    # 別表にしている人は、外部キーとして呼び出す値を得る
    # getKey()メソッド(または関数)は自作する事
    foreignKey = self.getKey(kinds)

    #ユーザー
    user_id = self.User['user_id']

    #予定詳細
    memo = self.text.get("1.0","end-1c")

    # データベースに新規予定を挿入する
    pass
    connection = pymysql.connect(host = '127.0.0.1',
                                 user = 'root',
                                 password = '',
                                 db = 'apr01',
                                 charset = 'utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        # トランザクション開始
        connection.begin()

        with connection.cursor() as cursor:

            cursor = connection.cursor()

            # SQLの作成・定義
#            sql = "select * from schedule"
            sql = "select max(id) from schedule"

            # SQLの実行
            cursor.execute(sql)

            sql = "insert into schedule (days, kinds_id, user_id, memo) values('{}', {}, {}, '{}')".format(days, foreignKey, user_id, memo)

            # SQLの実行
            cursor.execute(sql)

            sql = "select * from schedule"

            # SQLの実行
            cursor.execute(sql)



            # 実行結果の受け取り(複数行の場合)
            results = cursor.fetchall()
            for i, row in enumerate(results):
                print(i, row)

            """
            # 実行結果の受け取り(一行の場合)
            result = cursor.fetchone()
            print(result)
            """

#            idx = results['max(id)']
#            print(idx)

#            sql = "insert into schedule(days, kinds, memo) values({}, {}, {})".format(days, kinds, memo)
#            cursor.execute(sql)

            #sql = "select * from schedule where days = '{}-{}-{}'".format(self.year, self.mon, self.today)
            #print(sql)

            #cursor.execute(sql)


        connection.commit()

    except Exception as e:
        print('error:', e)
        connection.rollback()
    finally:
        connection.close()
    # この行に制御が移った時点で、DBとの接続は切れている

    self.sub_win.destroy()


  #-----------------------------------------------------------------
  # 日付をクリックした際に呼びだされるメソッド（コールバック関数）
  #
  # event: 左クリックイベント <Button-1>
  def click(self, event):
    day = event.widget['text']
    if day != ' ':
      self.title['text'] = '{}年{}月{}日の予定'.format(self.year, self.mon, day)
      self.today = day

      self.schedule()
      self.userlist()


  #foreignKey = getKey(kinds)
  def getKey(self, x):
    connection = pymysql.connect(host = '127.0.0.1',
                                  user = 'root',
                                  password = '',
                                  db = 'apr01',
                                  charset = 'utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)
    
    #p:str
    p = 0
    try:
        # トランザクション開始
        connection.begin()

        with connection.cursor() as cursor:

            cursor = connection.cursor()
            sql = "select kinds_id from kinds_table where kinds = '{}' ".format(x)
            p = cursor.execute(sql)
            if p is None:
              p = ("種類がありません")
            print(p)

        connection.commit()

    except Exception as e:
        print('errorr:', e)
        connection.rollback()
    finally:
        connection.close()

    return p

def Main():
  root = tk.Tk()
  YicDiary(root)
  root.mainloop()

if __name__ == '__main__':
  Main()
