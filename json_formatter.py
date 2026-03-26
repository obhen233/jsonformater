import sys
import json
import os
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QPushButton, QLabel, 
                             QMessageBox, QSplitter, QTreeWidget,
                             QTreeWidgetItem, QTabWidget, QMenuBar, QMenu,
                             QAction, QFileDialog, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QTextCursor, QSyntaxHighlighter, QTextCharFormat, QIcon

# 定义翻译字典
TRANSLATIONS = {
    'zh': {
        # 窗口标题
        'window_title': 'JSON格式化工具',
        
        # 按钮
        'format': '格式化',
        'clear': '清空',
        'copy_result': '复制结果',
        'expand_all': '全部展开',
        'collapse_all': '全部折叠',
        
        # 标签
        'input_json': '输入JSON:',
        'formatted_output': '格式化输出:',
        'json_tree_structure': 'JSON树形结构:',
        
        # 选项卡
        'text_view': '文本视图',
        'tree_view': '树形视图',
        
        # 占位符
        'input_placeholder': '请在此输入JSON数据...\n\n支持拖拽文件到此区域',
        'output_placeholder': '格式化后的JSON将显示在这里...',
        
        # 树形视图
        'root_object': '根对象 {{...}}',
        'root_array': '根数组 [{} items]',
        'items': '项',
        
        # 菜单
        'file': '文件',
        'edit': '编辑',
        'language': '语言',
        'view': '查看',
        'help': '帮助',
        
        # 文件菜单
        'open_file': '打开文件',
        'save_result': '保存结果',
        'exit': '退出',
        
        # 编辑菜单
        'compress_json': '压缩JSON',
        'clear_all': '清空所有',
        
        # 语言菜单
        'chinese': '中文',
        'english': 'English',
        
        # 查看菜单
        'text_view_menu': '文本视图',
        'tree_view_menu': '树形视图',
        'expand_all_tree': '树形全部展开',
        'collapse_all_tree': '树形全部折叠',
        
        # 帮助菜单
        'usage_guide': '使用说明',
        'about': '关于',
        
        # 消息框
        'warning': '警告',
        'error': '错误',
        'info': '提示',
        'please_enter_json': '请输入JSON数据',
        'no_valid_result': '没有有效的格式化结果可保存',
        'copied_to_clipboard': '已复制到剪贴板',
        'no_content_to_copy': '没有可复制的内容',
        'open_json_file': '打开JSON文件',
        'save_json_file': '保存JSON文件',
        'json_files': 'JSON文件 (*.json);;所有文件 (*.*)',
        'cannot_open_file': '无法打开文件：{}',
        'cannot_save_file': '无法保存文件：{}',
        'cannot_load_file': '无法加载文件：{}',
        'please_drag_json': '请拖拽JSON格式的文件',
        'json_format_error': 'JSON格式错误：\n{}',
        'error_location': '\n\n错误位置：第{}行，第{}列',
        'nearby_code': '\n\n附近代码：',
        'json_parse_error': 'JSON解析错误',
        'unknown_error': '发生未知错误：{}',
        
        # 关于对话框
        'about_title': '关于',
        'about_content': """
        <h2>JSON格式化工具</h2>
        <p>版本 2.0</p>
        
        <h3>功能特点：</h3>
        <ul>
            <li>JSON格式化与美化</li>
            <li>树形结构查看JSON数据</li>
            <li>语法高亮显示</li>
            <li>错误定位与提示</li>
            <li>文件打开与保存</li>
            <li>支持复制结果</li>
            <li>支持拖拽文件</li>
            <li>支持JSON压缩</li>
            <li>支持中英文切换</li>
        </ul>
        
        <h3>快捷键：</h3>
        <ul>
            <li>Ctrl+O: 打开文件</li>
            <li>Ctrl+S: 保存结果</li>
            <li>Ctrl+F: 格式化JSON</li>
            <li>Ctrl+M: 压缩JSON</li>
            <li>Ctrl+1: 文本视图</li>
            <li>Ctrl+2: 树形视图</li>
            <li>Ctrl+Q: 退出程序</li>
            <li>F1: 查看帮助</li>
        </ul>
        
        <p>© 2026 JSON Formatter</p>
        """,
        
        # 使用说明
        'usage_content': """
        <h3>使用说明</h3>
        
        <b>1. 基本使用：</b><br>
        在左侧输入框中输入JSON数据，点击"格式化"按钮即可在右侧看到格式化结果。<br><br>
        
        <b>2. 树形视图：</b><br>
        点击"树形视图"选项卡，可以以树形结构查看JSON数据，支持展开/折叠节点。<br>
        可以使用"全部展开"和"全部折叠"按钮来控制树形结构的显示。<br><br>
        
        <b>3. 文件操作：</b><br>
        通过菜单栏的"文件"菜单，可以打开JSON文件或保存格式化结果。<br>
        也支持直接拖拽JSON文件到输入区域。<br><br>
        
        <b>4. 压缩功能：</b><br>
        点击菜单栏"编辑"->"压缩JSON"可以将JSON压缩为一行，节省空间。<br><br>
        
        <b>5. 语言切换：</b><br>
        点击菜单栏"语言"可以切换中英文界面。<br><br>
        
        <b>6. 快捷键：</b><br>
        • Ctrl+O: 打开文件<br>
        • Ctrl+S: 保存结果<br>
        • Ctrl+F: 格式化JSON<br>
        • Ctrl+M: 压缩JSON<br>
        • Ctrl+1: 切换到文本视图<br>
        • Ctrl+2: 切换到树形视图<br>
        • Ctrl+Q: 退出程序<br>
        • F1: 查看帮助<br><br>
        
        <b>7. 错误处理：</b><br>
        如果JSON格式错误，程序会提示具体的错误位置和附近代码，方便快速定位问题。
        """
    },
    'en': {
        # 窗口标题
        'window_title': 'JSON Formatter Tool',
        
        # 按钮
        'format': 'Format',
        'clear': 'Clear',
        'copy_result': 'Copy Result',
        'expand_all': 'Expand All',
        'collapse_all': 'Collapse All',
        
        # 标签
        'input_json': 'Input JSON:',
        'formatted_output': 'Formatted Output:',
        'json_tree_structure': 'JSON Tree Structure:',
        
        # 选项卡
        'text_view': 'Text View',
        'tree_view': 'Tree View',
        
        # 占位符
        'input_placeholder': 'Please enter JSON data here...\n\nSupport drag and drop files',
        'output_placeholder': 'Formatted JSON will be displayed here...',
        
        # 树形视图
        'root_object': 'Root Object {{...}}',
        'root_array': 'Root Array [{} items]',
        'items': 'items',
        
        # 菜单
        'file': 'File',
        'edit': 'Edit',
        'language': 'Language',
        'view': 'View',
        'help': 'Help',
        
        # 文件菜单
        'open_file': 'Open File',
        'save_result': 'Save Result',
        'exit': 'Exit',
        
        # 编辑菜单
        'compress_json': 'Compress JSON',
        'clear_all': 'Clear All',
        
        # 语言菜单
        'chinese': 'Chinese (中文)',
        'english': 'English',
        
        # 查看菜单
        'text_view_menu': 'Text View',
        'tree_view_menu': 'Tree View',
        'expand_all_tree': 'Expand All Tree',
        'collapse_all_tree': 'Collapse All Tree',
        
        # 帮助菜单
        'usage_guide': 'Usage Guide',
        'about': 'About',
        
        # 消息框
        'warning': 'Warning',
        'error': 'Error',
        'info': 'Info',
        'please_enter_json': 'Please enter JSON data',
        'no_valid_result': 'No valid formatted result to save',
        'copied_to_clipboard': 'Copied to clipboard',
        'no_content_to_copy': 'No content to copy',
        'open_json_file': 'Open JSON File',
        'save_json_file': 'Save JSON File',
        'json_files': 'JSON Files (*.json);;All Files (*.*)',
        'cannot_open_file': 'Cannot open file: {}',
        'cannot_save_file': 'Cannot save file: {}',
        'cannot_load_file': 'Cannot load file: {}',
        'please_drag_json': 'Please drag JSON format files',
        'json_format_error': 'JSON format error:\n{}',
        'error_location': '\n\nError location: Line {}, Column {}',
        'nearby_code': '\n\nNearby code:',
        'json_parse_error': 'JSON Parse Error',
        'unknown_error': 'Unknown error: {}',
        
        # 关于对话框
        'about_title': 'About',
        'about_content': """
        <h2>JSON Formatter Tool</h2>
        <p>Version 2.0</p>
        
        <h3>Features:</h3>
        <ul>
            <li>JSON Formatting and Beautification</li>
            <li>Tree Structure View</li>
            <li>Syntax Highlighting</li>
            <li>Error Location and Prompt</li>
            <li>File Open and Save</li>
            <li>Copy Result</li>
            <li>Drag and Drop Support</li>
            <li>JSON Compression</li>
            <li>Multi-language Support (Chinese/English)</li>
        </ul>
        
        <h3>Shortcuts:</h3>
        <ul>
            <li>Ctrl+O: Open File</li>
            <li>Ctrl+S: Save Result</li>
            <li>Ctrl+F: Format JSON</li>
            <li>Ctrl+M: Compress JSON</li>
            <li>Ctrl+1: Text View</li>
            <li>Ctrl+2: Tree View</li>
            <li>Ctrl+Q: Exit</li>
            <li>F1: Help</li>
        </ul>
        
        <p>© 2026 JSON Formatter</p>
        """,
        
        # 使用说明
        'usage_content': """
        <h3>Usage Guide</h3>
        
        <b>1. Basic Usage:</b><br>
        Enter JSON data in the left input box, click the "Format" button to see the formatted result on the right.<br><br>
        
        <b>2. Tree View:</b><br>
        Click the "Tree View" tab to view JSON data in a tree structure, supports expand/collapse nodes.<br>
        Use the "Expand All" and "Collapse All" buttons to control tree display.<br><br>
        
        <b>3. File Operations:</b><br>
        Use the "File" menu to open JSON files or save formatted results.<br>
        Also supports dragging JSON files directly to the input area.<br><br>
        
        <b>4. Compression:</b><br>
        Click "Edit" -> "Compress JSON" to compress JSON to a single line.<br><br>
        
        <b>5. Language Switch:</b><br>
        Use the "Language" menu to switch between Chinese and English.<br><br>
        
        <b>6. Shortcuts:</b><br>
        • Ctrl+O: Open File<br>
        • Ctrl+S: Save Result<br>
        • Ctrl+F: Format JSON<br>
        • Ctrl+M: Compress JSON<br>
        • Ctrl+1: Switch to Text View<br>
        • Ctrl+2: Switch to Tree View<br>
        • Ctrl+Q: Exit Program<br>
        • F1: View Help<br><br>
        
        <b>7. Error Handling:</b><br>
        If the JSON format is incorrect, the program will prompt the specific error location and nearby code.
        """
    }
}

class JsonHighlighter(QSyntaxHighlighter):
    """JSON语法高亮器"""
    def __init__(self, parent=None):
        super(JsonHighlighter, self).__init__(parent)
        
        # 设置高亮格式
        self.key_format = QTextCharFormat()
        self.key_format.setForeground(QColor(0, 128, 0))  # 绿色
        
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor(255, 128, 0))  # 橙色
        
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor(0, 0, 255))  # 蓝色
        
        self.bool_format = QTextCharFormat()
        self.bool_format.setForeground(QColor(255, 0, 255))  # 紫色
        
        self.null_format = QTextCharFormat()
        self.null_format.setForeground(QColor(128, 128, 128))  # 灰色
        
    def highlightBlock(self, text):
        """高亮文本块"""
        # 高亮键名
        key_pattern = re.compile(r'"([^"\\]*(\\.[^"\\]*)*)"\s*:')
        for match in key_pattern.finditer(text):
            start = match.start()
            length = match.end() - start - 1
            self.setFormat(start, length, self.key_format)
        
        # 高亮字符串值
        string_pattern = re.compile(r':\s*"([^"\\]*(\\.[^"\\]*)*)"')
        for match in string_pattern.finditer(text):
            start = match.start(1)
            length = match.end() - start
            self.setFormat(start, length, self.string_format)
        
        # 高亮数字
        number_pattern = re.compile(r':\s*(-?\d+\.?\d*)')
        for match in number_pattern.finditer(text):
            start = match.start(1)
            length = match.end() - start
            self.setFormat(start, length, self.number_format)
        
        # 高亮布尔值
        bool_pattern = re.compile(r':\s*(true|false)')
        for match in bool_pattern.finditer(text):
            start = match.start(1)
            length = match.end() - start
            self.setFormat(start, length, self.bool_format)
        
        # 高亮null
        null_pattern = re.compile(r':\s*(null)')
        for match in null_pattern.finditer(text):
            start = match.start(1)
            length = match.end() - start
            self.setFormat(start, length, self.null_format)

class JsonTreeWidget(QTreeWidget):
    """JSON树形结构显示组件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setFont(QFont('Consolas', 10))
        self.setIndentation(20)
        self.setItemsExpandable(True)
        self.setExpandsOnDoubleClick(True)
        self.update_language()
        
    def update_language(self):
        """更新语言"""
        if self.parent_window:
            self.setHeaderLabel(self.parent_window.tr('json_tree_structure'))
    
    def load_json_data(self, json_data):
        """加载JSON数据到树形结构"""
        self.clear()
        
        # 创建根节点
        root_item = QTreeWidgetItem(self)
        
        if isinstance(json_data, dict):
            root_item.setText(0, self.parent_window.tr('root_object'))
            root_item.setForeground(0, QColor(0, 0, 255))
            root_item.setExpanded(True)
            self._add_dict_items(root_item, json_data)
        elif isinstance(json_data, list):
            root_item.setText(0, self.parent_window.tr('root_array').format(len(json_data)))
            root_item.setForeground(0, QColor(0, 0, 255))
            root_item.setExpanded(True)
            self._add_list_items(root_item, json_data)
        else:
            root_item.setText(0, str(json_data))
            root_item.setForeground(0, QColor(0, 0, 255))
    
    def _add_dict_items(self, parent, data):
        """添加字典项"""
        for key, value in data.items():
            display_key = f'"{key}"'
            if isinstance(value, dict):
                item = QTreeWidgetItem(parent)
                item.setText(0, f"{display_key}: {{...}}")
                item.setForeground(0, QColor(0, 128, 0))
                self._add_dict_items(item, value)
            elif isinstance(value, list):
                item = QTreeWidgetItem(parent)
                item.setText(0, f"{display_key}: [{len(value)} {self.parent_window.tr('items')}]")
                item.setForeground(0, QColor(0, 128, 0))
                self._add_list_items(item, value)
            else:
                item = QTreeWidgetItem(parent)
                item.setText(0, f"{display_key}: {self._format_value(value)}")
                item.setForeground(0, QColor(0, 128, 0))
                self._set_value_color(item, value)
    
    def _add_list_items(self, parent, data):
        """添加列表项"""
        for index, value in enumerate(data):
            display_index = f"[{index}]"
            if isinstance(value, dict):
                item = QTreeWidgetItem(parent)
                item.setText(0, f"{display_index}: {{...}}")
                item.setForeground(0, QColor(128, 0, 128))
                self._add_dict_items(item, value)
            elif isinstance(value, list):
                item = QTreeWidgetItem(parent)
                item.setText(0, f"{display_index}: [{len(value)} {self.parent_window.tr('items')}]")
                item.setForeground(0, QColor(128, 0, 128))
                self._add_list_items(item, value)
            else:
                item = QTreeWidgetItem(parent)
                item.setText(0, f"{display_index}: {self._format_value(value)}")
                item.setForeground(0, QColor(128, 0, 128))
                self._set_value_color(item, value)
    
    def _format_value(self, value):
        """格式化值显示"""
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, bool):
            return str(value).lower()
        elif value is None:
            return "null"
        else:
            return str(value)
    
    def _set_value_color(self, item, value):
        """设置值的颜色"""
        if isinstance(value, str):
            item.setForeground(0, QColor(255, 128, 0))
        elif isinstance(value, (int, float)):
            item.setForeground(0, QColor(0, 0, 255))
        elif isinstance(value, bool):
            item.setForeground(0, QColor(255, 0, 255))
        elif value is None:
            item.setForeground(0, QColor(128, 128, 128))

class JsonFormatter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_json_data = None
        self.current_lang = 'zh'  # 默认中文
        self.initUI()
        
    def tr(self, key):
        """翻译函数"""
        if self.current_lang in TRANSLATIONS and key in TRANSLATIONS[self.current_lang]:
            return TRANSLATIONS[self.current_lang][key]
        return key
        
    def initUI(self):
        """初始化UI"""
        self.setWindowTitle(self.tr('window_title'))
        self.setGeometry(100, 100, 1400, 900)
        
        # 设置窗口图标
        self.set_window_icon()
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 创建选项卡
        self.tab_widget = QTabWidget()
        
        # 左右窗口布局（文本视图）
        text_widget = QWidget()
        text_layout = QHBoxLayout()
        text_widget.setLayout(text_layout)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧输入区域
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        
        self.left_label = QLabel(self.tr('input_json'))
        self.left_label.setStyleSheet("font-weight: bold; font-size: 12px; padding: 5px;")
        left_layout.addWidget(self.left_label)
        
        self.input_text = QTextEdit()
        self.input_text.setFont(QFont('Consolas', 10))
        self.input_text.setPlaceholderText(self.tr('input_placeholder'))
        self.input_text.setAcceptDrops(True)
        left_layout.addWidget(self.input_text)
        
        # 右侧输出区域（文本视图）
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        
        self.right_label = QLabel(self.tr('formatted_output'))
        self.right_label.setStyleSheet("font-weight: bold; font-size: 12px; padding: 5px;")
        right_layout.addWidget(self.right_label)
        
        self.output_text = QTextEdit()
        self.output_text.setFont(QFont('Consolas', 10))
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText(self.tr('output_placeholder'))
        right_layout.addWidget(self.output_text)
        
        # 应用语法高亮
        self.json_highlighter = JsonHighlighter(self.output_text.document())
        
        # 添加部件到分割器
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([700, 700])
        
        text_layout.addWidget(splitter)
        
        # 树形结构视图
        tree_widget = QWidget()
        tree_layout = QVBoxLayout()
        tree_widget.setLayout(tree_layout)
        
        self.tree_label = QLabel(self.tr('json_tree_structure'))
        self.tree_label.setStyleSheet("font-weight: bold; font-size: 12px; padding: 5px;")
        tree_layout.addWidget(self.tree_label)
        
        self.tree_view = JsonTreeWidget(self)
        tree_layout.addWidget(self.tree_view)
        
        # 树形视图工具栏
        tree_toolbar = QHBoxLayout()
        self.expand_all_btn = QPushButton(self.tr('expand_all'))
        self.expand_all_btn.clicked.connect(self.expand_all_tree)
        self.expand_all_btn.setStyleSheet(self.get_small_button_style())
        tree_toolbar.addWidget(self.expand_all_btn)
        
        self.collapse_all_btn = QPushButton(self.tr('collapse_all'))
        self.collapse_all_btn.clicked.connect(self.collapse_all_tree)
        self.collapse_all_btn.setStyleSheet(self.get_small_button_style())
        tree_toolbar.addWidget(self.collapse_all_btn)
        
        tree_toolbar.addStretch()
        tree_layout.addLayout(tree_toolbar)
        
        # 添加选项卡
        self.tab_widget.addTab(text_widget, self.tr("text_view"))
        self.tab_widget.addTab(tree_widget, self.tr("tree_view"))
        
        main_layout.addWidget(self.tab_widget)
        
        # 主按钮区域
        button_layout = QHBoxLayout()
        
        self.format_btn = QPushButton(self.tr('format'))
        self.format_btn.setStyleSheet(self.get_main_button_style('#4CAF50', '#45a049', '#3d8b40'))
        self.format_btn.clicked.connect(self.format_json)
        button_layout.addWidget(self.format_btn)
        
        self.clear_btn = QPushButton(self.tr('clear'))
        self.clear_btn.setStyleSheet(self.get_main_button_style('#f44336', '#da190b', '#c62828'))
        self.clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_btn)
        
        self.copy_btn = QPushButton(self.tr('copy_result'))
        self.copy_btn.setStyleSheet(self.get_main_button_style('#2196F3', '#0b7dda', '#0a6ebd'))
        self.copy_btn.clicked.connect(self.copy_result)
        button_layout.addWidget(self.copy_btn)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTextEdit {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
            }
            QTextEdit:focus {
                border-color: #4CAF50;
            }
            QLabel {
                color: #333;
                padding: 5px;
            }
            QTabWidget::pane {
                border: 1px solid #d0d0d0;
                background-color: white;
                border-radius: 4px;
            }
            QTabBar::tab {
                padding: 8px 20px;
                background-color: #e8e8e8;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #4CAF50;
            }
            QTabBar::tab:hover {
                background-color: #d0d0d0;
            }
            QTreeWidget {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QTreeWidget::item {
                padding: 2px;
            }
            QTreeWidget::item:hover {
                background-color: #f0f0f0;
            }
            QMenuBar {
                background-color: #f8f8f8;
                border-bottom: 1px solid #d0d0d0;
            }
            QMenuBar::item {
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #e0e0e0;
            }
            QMenu {
                background-color: white;
                border: 1px solid #d0d0d0;
            }
            QMenu::item:selected {
                background-color: #4CAF50;
                color: white;
            }
        """)
    
    def get_small_button_style(self):
        """获取小按钮样式"""
        return """
            QPushButton {
                background-color: #e0e0e0;
                color: #333;
                border: 1px solid #ccc;
                padding: 4px 12px;
                font-size: 11px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
        """
    
    def get_main_button_style(self, bg_color, hover_color, pressed_color):
        """获取主按钮样式"""
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                padding: 10px 24px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
        """
    
    def set_window_icon(self):
        """设置窗口图标"""
        icon_paths = [
            'icon.ico',
            './icon.ico',
            os.path.join(os.path.dirname(__file__), 'icon.ico'),
            os.path.join(sys._MEIPASS, 'icon.ico') if hasattr(sys, '_MEIPASS') else None,
            os.path.join(os.path.dirname(sys.executable), 'icon.ico'),
        ]
        
        for icon_path in icon_paths:
            if icon_path and os.path.exists(icon_path):
                try:
                    self.setWindowIcon(QIcon(icon_path))
                    return
                except Exception:
                    pass
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        self.file_menu = menubar.addMenu(self.tr('file'))
        
        open_action = QAction(self.tr('open_file'), self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        self.file_menu.addAction(open_action)
        
        save_action = QAction(self.tr('save_result'), self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_result)
        self.file_menu.addAction(save_action)
        
        self.file_menu.addSeparator()
        
        exit_action = QAction(self.tr('exit'), self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)
        
        # 编辑菜单
        self.edit_menu = menubar.addMenu(self.tr('edit'))
        
        format_action = QAction(self.tr('format'), self)
        format_action.setShortcut('Ctrl+F')
        format_action.triggered.connect(self.format_json)
        self.edit_menu.addAction(format_action)
        
        compress_action = QAction(self.tr('compress_json'), self)
        compress_action.setShortcut('Ctrl+M')
        compress_action.triggered.connect(self.compress_json)
        self.edit_menu.addAction(compress_action)
        
        self.edit_menu.addSeparator()
        
        clear_all_action = QAction(self.tr('clear_all'), self)
        clear_all_action.triggered.connect(self.clear_all)
        self.edit_menu.addAction(clear_all_action)
        
        # 语言菜单
        self.language_menu = menubar.addMenu(self.tr('language'))
        
        chinese_action = QAction(self.tr('chinese'), self)
        chinese_action.triggered.connect(lambda: self.switch_language('zh'))
        self.language_menu.addAction(chinese_action)
        
        english_action = QAction(self.tr('english'), self)
        english_action.triggered.connect(lambda: self.switch_language('en'))
        self.language_menu.addAction(english_action)
        
        # 查看菜单
        self.view_menu = menubar.addMenu(self.tr('view'))
        
        text_view_action = QAction(self.tr('text_view_menu'), self)
        text_view_action.setShortcut('Ctrl+1')
        text_view_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(0))
        self.view_menu.addAction(text_view_action)
        
        tree_view_action = QAction(self.tr('tree_view_menu'), self)
        tree_view_action.setShortcut('Ctrl+2')
        tree_view_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(1))
        self.view_menu.addAction(tree_view_action)
        
        self.view_menu.addSeparator()
        
        expand_all_action = QAction(self.tr('expand_all_tree'), self)
        expand_all_action.triggered.connect(self.expand_all_tree)
        self.view_menu.addAction(expand_all_action)
        
        collapse_all_action = QAction(self.tr('collapse_all_tree'), self)
        collapse_all_action.triggered.connect(self.collapse_all_tree)
        self.view_menu.addAction(collapse_all_action)
        
        # 帮助菜单
        self.help_menu = menubar.addMenu(self.tr('help'))
        
        usage_action = QAction(self.tr('usage_guide'), self)
        usage_action.setShortcut('F1')
        usage_action.triggered.connect(self.show_usage)
        self.help_menu.addAction(usage_action)
        
        about_action = QAction(self.tr('about'), self)
        about_action.triggered.connect(self.show_about)
        self.help_menu.addAction(about_action)
    
    def switch_language(self, language):
        """切换语言"""
        self.current_lang = language
        
        # 更新窗口标题
        self.setWindowTitle(self.tr('window_title'))
        
        # 更新标签
        self.left_label.setText(self.tr('input_json'))
        self.right_label.setText(self.tr('formatted_output'))
        self.tree_label.setText(self.tr('json_tree_structure'))
        
        # 更新按钮
        self.format_btn.setText(self.tr('format'))
        self.clear_btn.setText(self.tr('clear'))
        self.copy_btn.setText(self.tr('copy_result'))
        self.expand_all_btn.setText(self.tr('expand_all'))
        self.collapse_all_btn.setText(self.tr('collapse_all'))
        
        # 更新选项卡
        self.tab_widget.setTabText(0, self.tr("text_view"))
        self.tab_widget.setTabText(1, self.tr("tree_view"))
        
        # 更新占位符
        self.input_text.setPlaceholderText(self.tr('input_placeholder'))
        self.output_text.setPlaceholderText(self.tr('output_placeholder'))
        
        # 更新树形视图标题
        self.tree_view.update_language()
        
        # 更新菜单栏
        self.file_menu.setTitle(self.tr('file'))
        self.edit_menu.setTitle(self.tr('edit'))
        self.language_menu.setTitle(self.tr('language'))
        self.view_menu.setTitle(self.tr('view'))
        self.help_menu.setTitle(self.tr('help'))
        
        # 更新菜单项
        for action in self.file_menu.actions():
            if action.text() in ['打开文件', 'Open File']:
                action.setText(self.tr('open_file'))
            elif action.text() in ['保存结果', 'Save Result']:
                action.setText(self.tr('save_result'))
            elif action.text() in ['退出', 'Exit']:
                action.setText(self.tr('exit'))
        
        for action in self.edit_menu.actions():
            if action.text() in ['格式化', 'Format']:
                action.setText(self.tr('format'))
            elif action.text() in ['压缩JSON', 'Compress JSON']:
                action.setText(self.tr('compress_json'))
            elif action.text() in ['清空所有', 'Clear All']:
                action.setText(self.tr('clear_all'))
        
        for action in self.language_menu.actions():
            if action.text() in ['中文', 'Chinese (中文)']:
                action.setText(self.tr('chinese'))
            elif action.text() in ['English', 'English']:
                action.setText(self.tr('english'))
        
        for action in self.view_menu.actions():
            if action.text() in ['文本视图', 'Text View']:
                action.setText(self.tr('text_view_menu'))
            elif action.text() in ['树形视图', 'Tree View']:
                action.setText(self.tr('tree_view_menu'))
            elif action.text() in ['树形全部展开', 'Expand All Tree']:
                action.setText(self.tr('expand_all_tree'))
            elif action.text() in ['树形全部折叠', 'Collapse All Tree']:
                action.setText(self.tr('collapse_all_tree'))
        
        for action in self.help_menu.actions():
            if action.text() in ['使用说明', 'Usage Guide']:
                action.setText(self.tr('usage_guide'))
            elif action.text() in ['关于', 'About']:
                action.setText(self.tr('about'))
        
        # 重新加载树形视图数据以更新内部文本
        if self.current_json_data:
            self.tree_view.load_json_data(self.current_json_data)
    
    def expand_all_tree(self):
        """展开所有树形节点"""
        self.tree_view.expandAll()
    
    def collapse_all_tree(self):
        """折叠所有树形节点"""
        self.tree_view.collapseAll()
    
    def open_file(self):
        """打开JSON文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, self.tr('open_json_file'), '', self.tr('json_files')
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.input_text.setText(content)
            except Exception as e:
                QMessageBox.critical(self, self.tr('error'), self.tr('cannot_open_file').format(str(e)))
    
    def save_result(self):
        """保存格式化结果"""
        if self.tab_widget.currentIndex() == 0:
            output_data = self.output_text.toPlainText()
        else:
            output_data = self.output_text.toPlainText()
        
        if not output_data or output_data.startswith(self.tr('error：')):
            QMessageBox.warning(self, self.tr('warning'), self.tr('no_valid_result'))
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, self.tr('save_json_file'), '', self.tr('json_files')
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(output_data)
            except Exception as e:
                QMessageBox.critical(self, self.tr('error'), self.tr('cannot_save_file').format(str(e)))
    
    def compress_json(self):
        """压缩JSON"""
        input_data = self.input_text.toPlainText().strip()
        if not input_data:
            QMessageBox.warning(self, self.tr('warning'), self.tr('please_enter_json'))
            return
        
        try:
            json_data = json.loads(input_data)
            compressed_json = json.dumps(json_data, ensure_ascii=False, separators=(',', ':'))
            self.output_text.setText(compressed_json)
            self.current_json_data = json_data
            self.tree_view.load_json_data(json_data)
        except json.JSONDecodeError as e:
            self.show_json_error(e, input_data)
    
    def format_json(self):
        """格式化JSON"""
        input_data = self.input_text.toPlainText().strip()
        
        if not input_data:
            QMessageBox.warning(self, self.tr('warning'), self.tr('please_enter_json'))
            return
        
        try:
            # 解析JSON
            self.current_json_data = json.loads(input_data)
            # 格式化JSON（缩进2个空格）
            formatted_json = json.dumps(self.current_json_data, ensure_ascii=False, indent=2)
            
            # 显示格式化结果
            self.output_text.setText(formatted_json)
            
            # 更新树形结构
            self.tree_view.load_json_data(self.current_json_data)
            
            # 自动滚动到顶部
            self.output_text.moveCursor(QTextCursor.Start)
            
        except json.JSONDecodeError as e:
            self.show_json_error(e, input_data)
        except Exception as e:
            QMessageBox.critical(self, self.tr('error'), self.tr('unknown_error').format(str(e)))
    
    def show_json_error(self, e, input_data):
        """显示JSON错误信息"""
        error_msg = self.tr('json_format_error').format(str(e))
        
        # 定位错误位置
        error_pos = e.pos
        if error_pos >= 0:
            # 获取错误所在行
            lines = input_data[:error_pos].split('\n')
            line_num = len(lines)
            col_num = len(lines[-1]) if lines else 0
            error_msg += self.tr('error_location').format(line_num, col_num)
            
            # 显示错误行附近的内容
            all_lines = input_data.split('\n')
            if line_num <= len(all_lines):
                start_line = max(0, line_num - 2)
                end_line = min(len(all_lines), line_num + 1)
                error_msg += self.tr('nearby_code')
                for i in range(start_line, end_line):
                    prefix = ">>> " if i == line_num - 1 else "    "
                    error_msg += f"\n{prefix}{all_lines[i]}"
        
        # 显示错误提示
        QMessageBox.critical(self, self.tr('json_parse_error'), error_msg)
        
        # 在输出框显示错误信息
        self.output_text.setText(self.tr("Error: {}").format(error_msg))
        
        # 清空树形结构
        self.tree_view.clear()
    
    def clear_all(self):
        """清空所有内容"""
        self.input_text.clear()
        self.output_text.clear()
        self.tree_view.clear()
        self.current_json_data = None
    
    def copy_result(self):
        """复制结果到剪贴板"""
        if self.tab_widget.currentIndex() == 0:
            output_data = self.output_text.toPlainText()
        else:
            output_data = self.output_text.toPlainText()
        
        if output_data and not output_data.startswith(self.tr('Error：')):
            clipboard = QApplication.clipboard()
            clipboard.setText(output_data)
            QMessageBox.information(self, self.tr('info'), self.tr('copied_to_clipboard'))
        else:
            QMessageBox.information(self, self.tr('info'), self.tr('no_content_to_copy'))
    
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, self.tr('about_title'), self.tr('about_content'))
    
    def show_usage(self):
        """显示使用说明"""
        QMessageBox.information(self, self.tr('usage_guide'), self.tr('usage_content'))
    
    def dragEnterEvent(self, event):
        """拖拽进入事件"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        """拖拽释放事件"""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.endswith('.json'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.input_text.setText(content)
                except Exception as e:
                    QMessageBox.critical(self, self.tr('error'), self.tr('cannot_load_file').format(str(e)))
            else:
                QMessageBox.warning(self, self.tr('warning'), self.tr('please_drag_json'))

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # 设置应用程序图标
    icon_paths = ['icon.ico', './icon.ico']
    for icon_path in icon_paths:
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
            break
    
    window = JsonFormatter()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()