import configparser


def permissao_desenvolvedor(id_usuario) -> bool:
            config = configparser.ConfigParser()
            config.read('config.conf')
            desenvolvedores_ids = [e.strip() for e in config.get('PERMISSIONS', 'DEVELOPERS_ID').split(',')]
            for desenvolvedor_id in desenvolvedores_ids:
                desenvolvedor_id = int(desenvolvedor_id)
                if id_usuario== desenvolvedor_id:
                    return True
            return False
                

if __name__ == '__main__':
    print(permissao_desenvolvedor(383756503989092353))
    print(permissao_desenvolvedor(123456789))
    print(permissao_desenvolvedor(987654321))