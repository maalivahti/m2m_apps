from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.bottomsheet import MDBottomSheet
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IconLeftWidget, IconRightWidget
from kivymd.uix.screen import MDScreen
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.textfield import MDTextField

from store.objects_store import objects_acc, objects_bot
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView

Window.size = (360, 800)

KV = '''
<DetailObjectContent>
    adaptive_height: True
    orientation: 'vertical'
    md_bg_color: [1, 1, 1, .9]
    
    
<SettingsObjectContent>
    adaptive_height: True
    orientation: 'vertical'
    md_bg_color: [1, 1, 1, .9]    

    
<MyLabel>:

MDScreen:
    MDBottomNavigation:
        panel_color: '#fefefe'
        selected_color_background: [0, 0, 0, 0]
        text_color_active: [0, .49, .76, 1]                   

        MDBottomNavigationItem:
            id: objects_page
            name: 'objects'
            text: 'Объекты'
            icon: 'car-multiple'
            md_bg_color: [0, .49, .76, 1]
            
            MDGridLayout:
                pos_hint:{'x': 0, 'top': 1}
                size_hint: [1, .15]
                # size: [0, 150]
                cols: 1
                # md_bg_color: 'orange'
                
                MDBoxLayout:
                    size_hint: [1, .5]
                    MDAnchorLayout:
                        pos_hint:{'center_x': .5, 'top': 1}
                        
                        MDSegmentedControl:
                            pos_hint:{'center_x': .5, 'top': 1}
                            md_bg_color: [0, .41, .64, 1]
                            segment_panel_height: '52dp'
                            on_active: app.on_active(*args)
            
                            MDSegmentedControlItem:
                                id: bot
                                text: 'М2МBOT'
            
                            MDSegmentedControlItem:
                                id: acc
                                text: 'Учетная запись'

                MDBoxLayout:
                    size_hint: [1, .5]
                    padding: [10, 0, 0, 0]
                    md_bg_color: [.2, .6, .8, 1]
    
                    MDTextField:
                        hint_text: "Поиск"
                        radius: [6, 6, 6, 6]
                        font_size: 12
                        pos_hint: {'x':0, 'center_y': .5}
                        helper_text: ""
                        icon_left: "magnify"
                        line_color_focus: [1, 1, 1, 1]
                        line_color_normal: [0, .49, .76, 1]
                        hint_text_color_normal: [1, 1, 1, 1]
                        icon_left_color_normal: [0, .49, .76, 1]
                        icon_left_color_focus: [1, 1, 1, 1]
                        text_color_focus: [1, 1, 1, 1]
                        text_color_normal: [1, 1, 1, 1]
                        on_text: app.search_objects(args[1])
                    
                    MDIconButton:
                        icon: "filter-variant"
                        pos_hint: {"x": 1, "center_y": .5}
                        theme_icon_color: "Custom"
                        icon_color: 'white'
                    
        MDBottomNavigationItem:
            name: 'statistics'
            text: 'Статистика'
            icon: 'chart-pie'

            MDLabel:
                text: 'Статистика'
                halign: 'center'  
                        
        MDBottomNavigationItem:
            name: 'reqTO'
            text: 'Заявки ТО'
            icon: 'list-box-outline'

            MDLabel:
                text: 'Заявки ТО'
                halign: 'center'

        MDBottomNavigationItem:
            name: 'reqTP'
            text: 'Заявки ТП'
            icon: 'list-box-outline'

            MDLabel:
                text: 'Заявки ТП'
                halign: 'center'        
'''

bot_list = objects_bot
acc_list = objects_acc


class ObjectScroller(MDScrollView):
    pass


class ListContainer(MDList):
    pass


class DetailObjectContent(MDBoxLayout):
    pass


class SettingsObjectContent(MDBoxLayout):
    pass


class DetailObjectHead(MDExpansionPanel):
    pass


# Создание списка параметров объекта для детализации
def create_obj_detail_list(detail_data):
    list = ListContainer()
    for prop in detail_data.items():
        list.add_widget(OneLineListItem(text=prop[0] + ' ' + prop[1]))
    return list


# Создание списка параметров объекта для настроек
def create_obj_settings_list(obj_data):
    list = DetailObjectContent()
    for prop in obj_data['object_data'].items():
        list.add_widget(MDTextField(hint_text=prop[0], text=prop[1]))
    return list


# Отображение окна настроек объекта
def show_alert_dialog(self):
    object = [obj for obj in objects_bot if obj.get('id') == self.id][0]
    self.dialog = MDDialog(
        title=f"Настройки объекта {object['name']}",
        type="custom",
        content_cls=create_obj_settings_list(object),
        buttons=[
            MDFlatButton(
                text="ОТМЕНИТЬ",
                theme_text_color="Custom",
                text_color=self.theme_cls.primary_color,
            ),
            MDFlatButton(
                text="СОХРАНИТЬ",
                theme_text_color="Custom",
                text_color=self.theme_cls.primary_color,
            ),
        ],
    )
    self.dialog.open()


# Создание списка объектов
def create_object_list(objects):
    obj_list = ListContainer()
    for object in objects:
        obj_detail_content = DetailObjectContent()
        obj_detail_content.add_widget(create_obj_detail_list(object['object_data']))
        obj_item = DetailObjectHead(content=obj_detail_content,
                              icon=object['img_url'],
                              panel_cls=MDExpansionPanelOneLine(
                                  IconRightWidget(
                                      id=object['id'],
                                      icon=object['right_icon'],
                                      on_release=show_alert_dialog,
                                  ),
                                  text=object['name'],
                                  bg_color=[.95, .95, .95, 1]))
        obj_list.add_widget(obj_item)

    return obj_list


# Загрузка списка объектов
def load_objects(self, obj_type, obj_list):
    if obj_type == 'bot':
        bot_scroll = ObjectScroller(size_hint=(1, .85))
        self.root.ids['object_bot'] = bot_scroll
        bot_scroll.add_widget(create_object_list(obj_list))
        self.root.ids.objects_page.add_widget(bot_scroll)
    elif obj_type == 'acc':
        acc_scroll = ObjectScroller(size_hint=(1, .85))
        self.root.ids['object_acc'] = acc_scroll
        acc_scroll.add_widget(create_object_list(obj_list))
        self.root.ids.objects_page.add_widget(acc_scroll)


class M2MApp(MDApp):
    object_active_tab = 'bot'

    def build(self):
        self.theme_cls.material_style = 'M3'
        return Builder.load_string(KV)

    def on_start(self):
        load_objects(self, self.object_active_tab, bot_list)
        # load_objects(self, self.object_active_tab, acc_list)

    def search_objects(self, value):
        obj_list = None
        if self.object_active_tab == 'bot':
            obj_list = [k for k in bot_list if value in k['name']]
            self.root.ids.object_bot.clear_widgets()
        else:
            obj_list = [k for k in acc_list if value in k['name']]
            self.root.ids.object_acc.clear_widgets()

        load_objects(self, self.object_active_tab, obj_list)

    def on_active(

            self,
            segmented_control: MDSegmentedControl,
            segmented_item: MDSegmentedControlItem,
    ) -> None:

        if segmented_item.text == 'М2МBOT':
            self.object_active_tab = 'bot'
            # print(self.root.ids.object_bot)
            # self.root.ids.object_bot.pos_hint = {'center_x': .5, 'top': .843}
            # self.root.ids.object_acc.pos_hint = {'x': 1, 'top': .843}
            root = self.root.ids.objects_page
            for child in root.children:
                print(child)
        else:
            self.object_active_tab = 'acc'
            # print(self.root.ids.object_acc)
            # self.root.ids.object_acc.pos_hint = {'center_x': .5, 'top': .843}
            # self.root.ids.object_bot.pos_hint = {'x': 1, 'top': .843}
            root = self.root.ids.objects_page
            for child in root.children:
                print(child)


M2MApp().run()

