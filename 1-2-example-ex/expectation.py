Ex().check_object('xpath').has_equal_value()
Ex().check_function('how_many_elements').has_equal_ast()
Ex().check_function('how_many_elements').has_equal_value()  # Не уверен в необходимости

success_msg("""
            Вы смогли обратиться ко всем дочерним элементам элемента body!
            Вам, должно быть, становится удобнее работать с символом подстановки!
            """)


