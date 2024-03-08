import form_executor

class NavSystem:
    def __init__(self, btn_ids:list, main_layout) -> None:
        self.btn_click_map = {btn:[None] for btn in btn_ids}
        self.current_layout = main_layout
        self.main_layout = main_layout
        self.stack =  []

    def get_back(self):
        form_executor.form_state = None
        try:
            previous = self.stack.pop()
        except IndexError:
            # print('Nothing to pop')
            self.current_layout = self.main_layout
            return self.current_layout()
        
        self.current_layout = previous
        return self.current_layout()


    def navigate_forward(self, layout_func, btn_id, n_clicks, form_state):        
        if self.btn_click_map[btn_id] == n_clicks or n_clicks == [] or n_clicks == [None]:
            self.btn_click_map[btn_id] = n_clicks
            return self.current_layout()
        
        form_executor.form_state = form_state
        self.btn_click_map[btn_id] = n_clicks
        self.stack.append(self.current_layout)
        self.current_layout = layout_func
        return self.current_layout()

