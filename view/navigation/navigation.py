from numbers import Number
from typing import List
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QStackedWidget, QWidget, QHBoxLayout
from PyQt5.QtCore import QSize, pyqtSignal

from model.app_feedback import AppFeedback
from model.data.device import Device
from view.navigation.navigation_page import NavigationPage
from view.navigation.navigation_item import NavigationItem, NavigationItemWidget
from view.navigation.navigation_pages import AppPages


# Returns an empty NavigationApp
def empty_navigation_app():
    return NavigationApp([])


class NavigationApp(QWidget):
    """ A wrapper class than enables navigation for the app, its given a list of pages that are of type (APage -> QWidget)   """

    navigator_history = [AppPages.SEATS.value]

    def __init__(self, pages: List[NavigationPage], parent=None):

        super().__init__(parent)
        # Main stack of pages
        self.stack = QStackedWidget()
        # List of navigation links
        self.side_nav = QListWidget()

        # Initializing the pages with the navigator so all pages can have access to it.
        self.pages = pages

        self.reset_page_stack()
        self.reset_nav_ui()

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.side_nav)
        self.layout.addWidget(self.stack)



    # clears the stack , appends the given pages to the stack
    def reset_page_stack(self):
        while self.stack.count() > 0:
            _pageWidget = self.stack.widget(0)
            self.stack.removeWidget(_pageWidget)
        for _page in self.pages:
            _page.initialize_navigator(self)
            self.stack.addWidget(_page)


    def refresh_ui(self):
        while self.stack.count() > 0:
            _pageWidget = self.stack.widget(0)
            self.stack.removeWidget(_pageWidget)

        # Removes all the subpages
        __pages = []
        for p in self.pages:
            if p.is_subpage:
                continue
            else:
                __pages.append(p)

        for _page in __pages:
            _page.initialize_navigator(self)
            _page.refresh_ui()
            self.stack.addWidget(_page)

        self.pages = __pages
        self.reset_nav_ui(AppPages.SEATS.value)

    # When feedback is received, finds the current page on display and gives it the feedback data to show
    def on_feedback(self,feedback: AppFeedback):
        for page in self.pages:
            if self.navigator_history[-1] == page.name:
                page.show_feedback(feedback)


    def clear_subpages(self,  _parent_page_name):
        __pages = []
        for  index,_p in enumerate(self.pages):
            is_sub_page_of_parent_page = _p.parent_page == _parent_page_name
            if is_sub_page_of_parent_page:
                # Remove any mention of the sub_page in history
                for _mention_index,history_mention in enumerate(self.navigator_history):
                    if history_mention == _p.name:
                        self.navigator_history.pop(_mention_index)
                continue
            else:
               __pages.append(_p)
        self.pages = __pages
        self.reset_page_stack()
        self.reset_nav_ui(_parent_page_name)

    def clear_page(self,_page_name,page_to_route_to):
        __pages = []
        for  index,_p in enumerate(self.pages):
            if _p.name == _page_name:
                # print("Found page to delete and going : " + _p.name)
                # Remove any mention of the page in history
                for _mention_index, history_mention in enumerate(self.navigator_history):
                    if history_mention == _p.name:
                        self.navigator_history.pop(_mention_index)
                continue
            else:
               __pages.append(_p)

        self.pages = __pages
        self.reset_page_stack()
        self.reset_nav_ui(page_to_route_to)

    def reset_nav_ui(self, default_page=AppPages.SEATS.value):
        # print("Resting and going : "+ default_page)
        self.side_nav.clear()
        self.side_nav.setFixedWidth(180)
        self.side_nav.setIconSize(QSize(24, 24))
        for page in  self.pages:

                # If their other pages referencing this page as a parent then this page is a parent
                _page_is_parent = any(_p.parent_page == page.name  for _p in self.pages)

                navItem = QListWidgetItem()
                navWidget = NavigationItemWidget(page_name=page.name, icon=page.icon, is_parent_page=_page_is_parent, is_subpage=page.is_subpage, clear_subpages_callback=self.clear_subpages,indent_level=self.get_page_indent_level(page))
                navItem.setSizeHint(navWidget.sizeHint())
                self.side_nav.addItem(navItem)
                self.side_nav.setItemWidget(navItem,navWidget)

        # self.side_nav.blockSignals(True)
        # print("Going to page : ###"+ str(self.get_page_index(default_page)))
        self.side_nav.setCurrentRow(self.get_page_index(default_page))
        # self.side_nav.blockSignals(False)
        self.side_nav.currentRowChanged.connect(self.nav_widget_change)



    # Check if navigator has history
    def navigator_has_history(self):
        return  len(self.navigator_history) > 1

    # Remove the last item from navigator_history , must only be called if self.navigation_history has a length of one or more
    def pop_nav_history(self):
        __history = self.navigator_history
        __history.pop()
        self.navigator_history = __history

    # Must be called only when self.navigator_has_history is true
    def go_back(self):
        # # Remove the current page and re-render the side_nav
        __currentPage = self.get_page_by_name(self.current_page_name())
        if __currentPage.is_subpage:
            # print("Using a subpage: " + __currentPage.name)
            self.pop_nav_history()
            previous_page = self.navigator_history[-1]
            self.clear_page(__currentPage.name,previous_page)
        else:
            self.pop_nav_history()
            previous_page = self.navigator_history[-1]
            self.go_to_page(previous_page)


    def get_page_index(self,page_name):
        for index,page in enumerate(self.pages):
            if page.name == page_name:
                return  index
        return  -1

    def get_page_by_index(self, index):
        return self.pages[index]

    def get_page_by_name(self, name):
        return self.pages[self.get_page_index(name)]

    def current_page_name(self):
        return self.navigator_history[-1]

    def nav_widget_change(self,index):
        # print("Went to #:  "+ str(index) + " name: "+ self.get_page_by_index(index).name)
        if index != -1:
            self.go_to_page(self.get_page_by_index(index).name)

    # All navigation must use this method
    def go_to_page(self, page_name):
            current_page = self.get_page_by_name(self.current_page_name())
            page_to_go_to = self.get_page_by_name(page_name)
            page_to_go_to_index = self.get_page_index(page_to_go_to.name)
            _page_to_go_to_is_not_current_page = current_page.name != page_to_go_to.name
            if  _page_to_go_to_is_not_current_page:
                # # If the page being added is a subpage make sure the previous page is the parent page
                # if (page_to_go_to.is_subpage and page_to_go_to.parent_page == current_page.name) or page_to_go_to.is_subpage == False:
                self.navigator_history.append(page_to_go_to.name)
                # print("  -> ".join(str(item) for item in self.navigator_history))

            self.pages[page_to_go_to_index].initialize_navigator(self)
            self.stack.setCurrentIndex(page_to_go_to_index)
            self.side_nav.setCurrentRow(page_to_go_to_index)


    #Goes to a subpage relative to this route, gets the subpage widget and constructs a navigation page based on the current page
    def go_to_subpage(self, parent_page, subpage_name:str, widget: QWidget):
        for index,page in enumerate(self.pages):
            print("Going to: "+ subpage_name + " Parent is : "+ parent_page)
            if page.name == parent_page:
                _page_already_exists = any(__p.name == subpage_name for __p in self.pages)
                if _page_already_exists:
                    self.go_to_page(subpage_name)
                else:
                    _subPage = NavigationPage(page.icon, subpage_name, page.name+ f" / "+ subpage_name, widget,True,page.name)
                    index_to_go_to = index+1

                    self.pages.insert(index_to_go_to, _subPage)
                    self.reset_page_stack()
                    self.reset_nav_ui(subpage_name)
                return


    def get_page_indent_level(self,page: NavigationPage) -> Number:
        current = page
        depth = 0

        while current.is_subpage:
            depth += 1
            current = self.get_page_by_name(current.parent_page)

        return depth