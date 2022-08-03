style_sheet = """
            
            
            QPushButton {
                    background-color : rgb(220, 50, 0);
                    border : none;
                    border-radius : 3px;
                    padding : 7px;
                    font-size : 14px;
                    color : white;
                    }
                    
            QPushButton:hover {
                    background-color : rgb(240, 50, 0);
                    border : 1px solid rgb(24, 70, 0)}
                    
            QPushButton:pressed {background-color : rgb(240, 80, 10);
                                border : 1px solid rgb(240, 0, 0)}
            
            QWidget#side_bar {background-color : rgb(0, 20, 100);
                                color : white;
                                margin : 0px;}
                                
            QWidget#main {background-image : url(images/system_images/wallpaper.jpg);
                            background-position : center center}    
            
            QPushButton#side_button {
                            background-color : rgb(0, 20, 100);
                            font-size : 17px;
                            border-radius : 0px;
                            }
                            
            QPushButton#side_button:hover , QPushButton#side_button:pressed 
                                    {background-color : rgb(0, 0, 150);
                                    border : none;}    
                        
            
            QDockWidget {
                    titlebar-close-icon : url(:/img/sys/close.png);
                    }
                                    
            QDockWidget::close-button {
                        background-color : rgb(20, 20, 20);
                        color : red;
                        padding : 5px;}        
            
            """