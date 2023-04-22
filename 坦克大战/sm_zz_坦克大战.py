# 世茫折纸&坦克大战&制作练习    ESC重生
import pygame, time, random
pygame.init()

窗口宽 = 800
窗口高 = 500
窗口颜色 = pygame.Color((0, 0, 0))
字体颜色 = pygame.Color(255, 0, 0)
字体位置 = (20, 15)
字体位置1 = (350, 230)

# FPS = 60  #
# clock = pygame.time.Clock()  #
#
# Z_PiMu_S1 = (0, 255, 0)  # 字体背景色
# Z_PiMu_S3 = (0, 0, 0)
# myFont = pygame.font.Font('C:/沐瞳/OneDrive/桌面/折纸折纸折纸/萝莉体.ttc', 30)
# cont = 0
# start = time.time()


# 定义一个基类
class BaseItem(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)


# pygame.sprite



class MainGame():
    window = None
    my_tanke = None
    # 存储敌方坦克的列表
    df_Tank_List = []
    # 定义敌方坦克的数量
    df_Tank_SuL = 10
    # 存储我方子弹列表
    myZhiDanList = []
    # 存储敌方子弹的列表
    dfZhiDanList = []
    # 存储爆炸列表
    baozaList = []
    # 存储墙壁的列表
    qiangbiList = []

    def __init__(self):
        pass


    # 开始游戏
    def startGame(self):
        global cont
        pygame.display.init()
        # 设置窗口的大小及显示     #加载主窗口 初始化
        MainGame.window = pygame.display.set_mode([窗口宽, 窗口高])
        # 初始化我方坦克
        self.create_Mytanke()
        # 初始化敌方坦克 并将敌方坦克添加到列表当中
        self.create_DifTk()
        # 初始化墙壁
        self.creatQiangbi()
        # 设置窗口标题
        pygame.display.set_caption('sm_zz.坦克大战')
        # 保持窗口一直开着
        while True:
            # cont += 1  #
            # now = time.time()  #
            # fps = (cont / (now - start)).__round__(2)  #
            # fpsImg = myFont.render('FPS:' + str(fps), True, Z_PiMu_S3)  #
            # fpsImg.get_rect()
            # screen.blit(fpsImg, (10, 5))

            # 使用坦克移动速度慢一点
            time.sleep(0.05)
            # 给窗口填充颜色
            MainGame.window.fill(窗口颜色)
            # 获取事件
            self.shijian()
            # 绘制文字
            MainGame.window.blit(self.wz_sl('敌方坦克剩余数量: %d' % len(MainGame.df_Tank_List)), 字体位置)
            # 判断我方坦克是否存活
            if MainGame.my_tanke and MainGame.my_tanke.live:
                MainGame.my_tanke.zs_Tanke()
            else:
                # 删除我方坦克
                del MainGame.my_tanke
                MainGame.my_tanke = None
            # 循环遍历列表展示敌方坦克
            self.blit_df_tk()
            # 循环遍历我方子弹
            self.blitMy_zd()
            # 循环遍历敌方子弹列表，展示敌方子弹
            self.blitDf_zd()
            # 循环遍历爆炸列表,展示爆炸效果
            self.blitBaozha()
            # 循环遍历墙壁列表,展示墙壁
            self.blitQiangbi()
            # 如果坦克的开关是开启的话，才可以移动否则不能移动
            if MainGame.my_tanke and MainGame.my_tanke.live:
                if not MainGame.my_tanke.stop:
                    MainGame.my_tanke.yidong()  # 调用移动方法
                    # 检测我方坦克是否与墙壁发生碰撞
                    MainGame.my_tanke.ZD_QB()
                    # 检测我方坦克是否与敌方坦克发生碰撞
                    MainGame.my_tanke.my_Tanke_df_Tanke()
            pygame.display.update()

    # 循环遍历墙壁列表,展示墙壁
    def blitQiangbi(self):
        for qiangbi in MainGame.qiangbiList:
            # 判断墙壁是否存活
            if qiangbi.live:
                # 调用墙壁
                qiangbi.zs_qiangbi()
            else:
                # 移除
                MainGame.qiangbiList.remove(qiangbi)

    # 初始化墙壁
    def creatQiangbi(self):
        for i in range(8):
            qiangbi = Qiangbi(i * 120, 200)
            # 将墙壁添加到链表中
            MainGame.qiangbiList.append(qiangbi)

    # 创建我方坦克的方法
    def create_Mytanke(self):
        MainGame.my_tanke = MyTanke(350, 250)

    # 初始化敌方坦克 并将敌方坦克添加到列表当中
    def create_DifTk(self):
        top = 100
        # 循环生成坦克
        for i in range(MainGame.df_Tank_SuL):
            left = random.randint(0, 600)
            speed = random.randint(1, 4)
            enemy = Df_Tanke(left, top, speed)
            MainGame.df_Tank_List.append(enemy)

    # 循环展示爆炸效果
    def blitBaozha(self):
        for baozha in MainGame.baozaList:
            # 判断是否活着
            if baozha.live:
                # 展示
                baozha.zs_baozha()
            else:
                # 移除
                MainGame.baozaList.remove(baozha)

    # 循环遍历列表展示敌方坦克
    def blit_df_tk(self):
        for df_Tanke in MainGame.df_Tank_List:
            # 判断当前敌方坦克是否活着
            if df_Tanke.live:
                df_Tanke.zs_Tanke()
                df_Tanke.d_yidong()
                # 调用检测是否与墙壁碰撞
                df_Tanke.ZD_QB()
                # 检测敌方坦克是否与我方子弹发生碰撞
                if MainGame.my_tanke and MainGame.my_tanke.live:
                    df_Tanke.dfTanke_myTanke()
                # 发射子弹
                df_Zhidan = df_Tanke.seji()
                if df_Zhidan:
                    # 将敌方子弹储存到敌方子弹列表中
                    MainGame.dfZhiDanList.append(df_Zhidan)
            else:  # 不活着，从敌方坦克列表中移除
                MainGame.df_Tank_List.remove(df_Tanke)

    # 循环遍历我方子弹存储列表
    def blitMy_zd(self):
        for my_zhidan in MainGame.myZhiDanList:
            # 判断当前的子弹是否是活着的状态，如果是则移动
            if my_zhidan.live:
                my_zhidan.zs_zhidan()
                # 调用子弹的移动方法
                my_zhidan.yidong()
                # 调用检测我方子弹是否与敌方坦克发生碰撞
                my_zhidan.myZhidan_pz_dfTanke()
                # 检测我方子弹是否与墙壁发生碰撞
                my_zhidan.ZD_QB()
            # 否则消失
            else:
                MainGame.myZhiDanList.remove(my_zhidan)

    # 循环遍历敌方子弹列表，展示敌方子弹
    def blitDf_zd(self):
        for df_zhidan in MainGame.dfZhiDanList:
            if df_zhidan.live:
                df_zhidan.zs_zhidan2()
                df_zhidan.yidong()
                # 调用敌方子弹与我方坦克碰撞的方法
                df_zhidan.dfZhidan_pz_myTanke()
                # 检测敌方子弹是否与墙壁发生碰撞
                df_zhidan.ZD_QB()
            else:
                MainGame.dfZhiDanList.remove(df_zhidan)

    # 结束游戏
    def endGame(self):
        print('成功退出')
        exit()

    # 左上角文字绘制
    def wz_sl(self, text):
        # 初始化字体模块
        pygame.font.init()
        # print (pygame.font.get_fonts()) #让我看看都有哪些字体 #还是下载的萝莉体好
        # 获取font对象
        font = pygame.font.Font('萝莉体.ttc', 18)
        # 绘制文字信息
        textSurface = font.render(text, True, 字体颜色)
        return textSurface

    # 获取事件
    def shijian(self):
        # 获取所有事件
        eventList = pygame.event.get()
        # 遍历事件
        for event in eventList:
            # 判断按下的键是关闭还是不是关闭
            # 如果是关闭则退出
            if event.type == pygame.QUIT:
                self.endGame()
            # 如果是键盘的按下
            if event.type == pygame.KEYDOWN:
                # 当坦克不存在死亡
                if not MainGame.my_tanke:
                    # 判断按下的是ESC重生
                    if event.key == pygame.K_ESCAPE:
                        # 让我方坦克重生及调用创建坦克的方法
                        self.create_Mytanke()
                if MainGame.my_tanke and MainGame.my_tanke.live:
                    # 判断按下的是 上 下 左 右
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        # 切换方向
                        MainGame.my_tanke.direction = '左'
                        # 开关状态
                        MainGame.my_tanke.stop = False
                        # MainGame.my_tanke.yidong() #丢弃的移动
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        MainGame.my_tanke.direction = '右'
                        MainGame.my_tanke.stop = False

                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        MainGame.my_tanke.direction = '上'
                        MainGame.my_tanke.stop = False

                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        MainGame.my_tanke.direction = '下'
                        MainGame.my_tanke.stop = False
                    # 空格键射子弹
                    elif event.key == pygame.K_SPACE:
                        # 如果当前我方子弹列表的大小 小于等于3的时候才可以创建
                        if len(MainGame.myZhiDanList) < 6:
                            # 创建我方发射子弹
                            zhidan = Zhidan(MainGame.my_tanke)
                            MainGame.myZhiDanList.append(zhidan)
                            # 我方坦克发射子弹添加音效
                            yinyue = Yinyue('图像与字体\鸡.mp3')
                            yinyue.bf_Yinyue()

            # 松开方向键坦克停止跑 #改 开关状态
            # 点击射击时不要停止跑
            if event.type == pygame.KEYUP:
                # 判断松开的键是上下左右，停止移动
                if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if MainGame.my_tanke and MainGame.my_tanke.live:
                        MainGame.my_tanke.stop = True


class Tanke(BaseItem):
    def __init__(self, left, top):
        # 保存加载的图片
        self.images = {'上': pygame.image.load('图像与字体/我方坦克上.png'),
                       '下': pygame.image.load('图像与字体/我方坦克下.png'),
                       '左': pygame.image.load('图像与字体/我方坦克左.png'),
                       '右': pygame.image.load('图像与字体/我方坦克右.png'), }
        # 方向
        self.direction = '上'
        # 根据当前图片的方向获取图片 surface
        self.image = self.images[self.direction]
        # 根据图片获取区域
        self.rect = self.image.get_rect()
        # 设置区域的 left和top
        self.rect.left = left
        self.rect.top = top
        # 速度
        self.speed = 10
        # 移动开关
        self.stop = True
        # 是否活着
        self.live = True
        # 原来的坐标
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

    # 移动
    def yidong(self):
        # 移动后记录原始坐标
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top
        # 判断坦克的方向进行移动
        if self.direction == '左':
            if self.rect.left > 0:
                self.rect.left -= self.speed

        elif self.direction == '上' and self.rect.top > 0:
            self.rect.top -= self.speed
        elif self.direction == '右' and self.rect.left < 670:
            self.rect.left += self.speed
        elif self.direction == '下' and self.rect.top < 470:
            self.rect.top += self.speed

    # 射击
    def seji(self):
        return Zhidan(self)

    def stay(self):
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop

    # 检测坦克是否与墙壁发生碰撞
    def ZD_QB(self):
        for qiangbi in MainGame.qiangbiList:
            if pygame.sprite.collide_rect(self, qiangbi):
                # 将坐标设置为移动之前的坐标
                self.stay()

    # 展示坦克的方法
    def zs_Tanke(self):
        # 获取展示对象
        self.image = self.images[self.direction]
        # 调用blit方法展示
        MainGame.window.blit(self.image, self.rect)


# 我方坦克
class MyTanke(Tanke):
    def __init__(self, left, top):
        super(MyTanke, self).__init__(left, top)
        # 创建音乐对象
        yiyue = Yinyue('图像与字体/坦克大战.mp3')
        # 播放音乐的方法
        yiyue.bf_Yinyue()

    # 检测我方坦克与敌方坦克发生碰撞
    def my_Tanke_df_Tanke(self):
        # 循环遍历敌方坦克列表
        for df_Tanke in MainGame.df_Tank_List:
            if pygame.sprite.collide_rect(self, df_Tanke):
                self.stay()

    # 移动类
    def w_yidong(self):
        pass


# 敌方坦克
def randDirection():
    num = random.randint(1, 4)
    if num == 1:
        return '上'
    elif num == 2:
        return '下'
    elif num == 3:
        return '左'
    elif num == 4:
        return '右'


class Df_Tanke(Tanke):
    def __init__(self, left, top, speed):
        # 调用父类的初始化方法
        super(Df_Tanke, self).__init__(left, top)
        # 加载图片集
        self.images = {'上': pygame.image.load('图像与字体/敌方坦克上.png'),
                       '下': pygame.image.load('图像与字体/敌方坦克下.png'),
                       '左': pygame.image.load('图像与字体/敌方坦克左.png'),
                       '右': pygame.image.load('图像与字体/敌方坦克右.png'),
                       }
        # 方向,随机生成坦克方向
        self.direction = randDirection()
        # 根据方向获取图片
        self.image = self.images[self.direction]
        # 区域
        self.rect = self.image.get_rect()
        # 对left和top进行赋值
        self.rect.left = left
        self.rect.top = top
        # 速度
        self.speed = speed
        # 移动开关键
        self.flag = True
        # 新增加一个步数变量 step
        self.step = 50

    # 敌方坦克与我方坦克发生碰撞
    def dfTanke_myTanke(self):
        if pygame.sprite.collide_rect(self, MainGame.my_tanke):
            self.stay()

    # 随机生成敌方坦克方向

    # 移动类
    def d_yidong(self):
        if self.step <= 0:
            # 修改方向
            self.direction = randDirection()
            # 步数复位
            self.step = 50
        else:
            self.yidong()
            # 让步数递减
        self.step -= 1

    # 重写seji()
    def seji(self):
        num = random.randint(1, 100)
        if num < 10:
            return Zhidan(self)


class Zhidan(BaseItem):
    def __init__(self, tanke):
        # 加载图片
        self.image = pygame.image.load('图像与字体/我方子弹.png')
        self.image2 = pygame.image.load('图像与字体/敌方子弹.png')
        # 坦克方向决定子弹方向
        self.direction = tanke.direction
        # 获取区域
        self.rect = self.image.get_rect()
        # 子弹的left和top与方向有关
        if self.direction == '上':
            self.rect.left = tanke.rect.left + tanke.rect.width / 2 - self.rect.width / 2
            self.rect.top = tanke.rect.top - self.rect.height
        elif self.direction == '下':
            self.rect.left = tanke.rect.left + tanke.rect.width / 2 - self.rect.width / 2
            self.rect.top = tanke.rect.top + self.rect.height
        elif self.direction == '左':
            self.rect.left = tanke.rect.left - tanke.rect.width / 2 - self.rect.width / 2
            self.rect.top = tanke.rect.top + self.rect.width / 2 - self.rect.width / 2
        elif self.direction == '右':
            self.rect.left = tanke.rect.left + tanke.rect.width
            self.rect.top = tanke.rect.top + self.rect.width / 2 - self.rect.width / 2
        # 子弹的速度
        self.speed = 12
        # 子弹状态，是否碰到墙壁，如果碰到墙壁，修改此状态
        self.live = True

    # 移动类
    def yidong(self):
        if self.direction == '上':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                # 修改子弹状态
                self.live = False
        elif self.direction == '下':
            if self.rect.top + self.rect.height < 窗口高 - 10:
                self.rect.top += self.speed
            else:
                self.live = False
        elif self.direction == '左':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.live = False
        elif self.direction == '右':
            if self.rect.left + self.rect.width < 窗口宽 - 10:
                self.rect.left += self.speed
            else:
                self.live = False

    # 子弹是否碰撞墙壁
    def ZD_QB(self):
        # 循环遍历墙壁列表
        for qiangbi in MainGame.qiangbiList:
            if pygame.sprite.collide_rect(self, qiangbi):
                # 修改子弹的生存状态，让子弹消失
                self.live = False
                qiangbi.hp -= 1
                if qiangbi.hp <= 0:
                    # 修改墙壁的生存状态
                    qiangbi.live = False

    # 展示子弹的方法
    def zs_zhidan(self):
        # 将图片加载到窗口
        MainGame.window.blit(self.image, self.rect)

    # 展示子弹的方法
    def zs_zhidan2(self):
        # 将图片加载到窗口
        MainGame.window.blit(self.image2, self.rect)

    # 我方子弹与敌方坦克的碰撞
    def myZhidan_pz_dfTanke(self):
        # 循环遍历敌方坦克列表，判断是否发生碰撞
        for df_Tanke in MainGame.df_Tank_List:
            if pygame.sprite.collide_rect(df_Tanke, self):
                # 修改敌方坦克和我方子弹状态
                df_Tanke.live = False
                self.live = False
                # 创建爆炸对象
                baozha = Baozha(df_Tanke)
                # 将爆炸对象添加到爆炸列表当中
                MainGame.baozaList.append(baozha)

    # 敌方子弹与我方子弹发生碰撞
    def dfZhidan_pz_myTanke(self):
        if MainGame.my_tanke and MainGame.my_tanke.live:
            if pygame.sprite.collide_rect(MainGame.my_tanke, self):
                # 产生爆炸对象
                baoza = Baozha(MainGame.my_tanke)
                # 将爆炸对象添加到爆炸列表当中
                MainGame.baozaList.append(baoza)
                # 修改敌方子弹与我方坦克的状态
                self.live = False
                MainGame.my_tanke.live = False


class Qiangbi():
    def __init__(self, left, top):
        # 加载墙壁图片
        self.image = pygame.image.load('图像与字体/墙.png')
        # 获取墙壁的区域
        self.rect = self.image.get_rect()
        # 设置位置
        self.rect.left = left
        self.rect.top = top
        # 是否存活
        self.live = True
        # 设置生命值
        self.hp = 3

    # 展示墙壁的方法
    def zs_qiangbi(self):
        MainGame.window.blit(self.image, self.rect)


class Baozha():
    def __init__(self, tanke):
        self.rect = tanke.rect
        self.imangs = [
            pygame.image.load('图像与字体/爆炸.png'),
            pygame.image.load('图像与字体/爆炸.png'),
            pygame.image.load('图像与字体/爆炸.png'),
            pygame.image.load('图像与字体/爆炸.png'),
        ]
        self.step = 0
        # 是否活着
        self.live = True

    # 展示爆炸类效果
    def zs_baozha(self):
        if self.step < len(self.imangs):
            # 根据索引获取爆炸对象
            self.image = self.imangs[self.step]
            self.step += 1
            # 添加到主窗口
            MainGame.window.blit(self.image, self.rect)
        else:
            # 修改状态
            self.live = False
            self.step = 0


class Yinyue:
    def __init__(self, yyname):
        self.yyname = yyname
        # 初始化音乐混合器
        pygame.mixer.init()
        # 加载音乐
        pygame.mixer.music.load(self.yyname)

    # 播放音乐
    def bf_Yinyue(self):
        pygame.mixer.music.play()


if __name__ == '__main__':

    MainGame().startGame()
