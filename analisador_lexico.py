import re
from collections import namedtuple
import sys
import os

# Definir os tokens
Token = namedtuple('Token', ['type', 'value', 'line', 'column'])

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.line = 1
        self.column = 1
        self.pos = 0
        
        # Definir padrões de tokens (regex) - ORDEM É IMPORTANTE!
        self.token_specs = [
            ('NUMBER',   r'\d+(\.\d*)?'),          # Números inteiros ou decimais
            ('IDENT',    r'[a-zA-Z_]\w*'),         # Identificadores
            ('EQ',       r'=='),                   # Igualdade
            ('NE',       r'!='),                   # Diferente
            ('LTE',      r'<='),                   # Menor ou igual
            ('GTE',      r'>='),                   # Maior ou igual
            ('LT',       r'<'),                    # Menor que
            ('GT',       r'>'),                    # Maior que
            ('ASSIGN',   r'='),                    # Atribuição
            ('OP',       r'[+\-*/%]'),             # Operadores aritméticos
            ('LPAREN',   r'\('),                   # Parêntese esquerdo
            ('RPAREN',   r'\)'),                   # Parêntese direito
            ('LBRACKET', r'\['),                   # Colchete esquerdo
            ('RBRACKET', r'\]'),                   # Colchete direito
            ('LBRACE',   r'\{'),                   # Chave esquerda
            ('RBRACE',   r'\}'),                   # Chave direita
            ('SEMI',     r';'),                    # Ponto e vírgula
            ('COMMA',    r','),                    # Vírgula
            ('COLON',    r':'),                    # Dois pontos
            ('DOT',      r'\.'),                   # Ponto
            ('STRING',   r'\"[^\"]*\"|\'[^\']*\''), # Strings (simples ou duplas)
            ('COMMENT',  r'#.*'),                  # Comentários de linha
            ('MULTICOMMENT', r'\'\'\'.*?\'\'\'|\"\"\".*?\"\"\"', re.DOTALL), # Comentários múltiplas linhas
            ('WHITESPACE', r'\s+'),                # Espaços em branco
            ('MISMATCH', r'.'),                    # Qualquer outro caractere
        ]
        
        # Compilar regex
        self.regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.token_specs if isinstance(pair[1], str))
        self.pattern = re.compile(self.regex)
    
    def tokenize(self):
        for match in self.pattern.finditer(self.code):
            kind = match.lastgroup
            value = match.group()
            
            # Calcular coluna atual
            line_start = self.code.rfind('\n', 0, match.start()) + 1
            current_column = match.start() - line_start + 1
            
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
                self.tokens.append(Token('NUMBER', value, self.line, current_column))
            elif kind == 'IDENT':
                # Verificar palavras reservadas
                keywords = {
                    'if': 'KEYWORD', 
                    'else': 'KEYWORD', 
                    'elif': 'KEYWORD',
                    'while': 'KEYWORD', 
                    'for': 'KEYWORD', 
                    'def': 'KEYWORD',
                    'return': 'KEYWORD',
                    'print': 'KEYWORD',
                    'True': 'BOOLEAN',
                    'False': 'BOOLEAN',
                    'None': 'KEYWORD',
                    'import': 'KEYWORD',
                    'from': 'KEYWORD',
                    'as': 'KEYWORD',
                    'class': 'KEYWORD',
                    'try': 'KEYWORD',
                    'except': 'KEYWORD',
                    'finally': 'KEYWORD',
                    'with': 'KEYWORD',
                    'lambda': 'KEYWORD',
                    'and': 'OPERATOR',
                    'or': 'OPERATOR',
                    'not': 'OPERATOR',
                    'in': 'OPERATOR',
                    'is': 'OPERATOR'
                }
                if value in keywords:
                    self.tokens.append(Token(keywords[value], value, self.line, current_column))
                else:
                    self.tokens.append(Token('IDENT', value, self.line, current_column))
            elif kind == 'STRING':
                # Remover aspas
                self.tokens.append(Token('STRING', value[1:-1], self.line, current_column))
            elif kind == 'COMMENT' or kind == 'MULTICOMMENT':
                continue  # Ignorar comentários
            elif kind == 'WHITESPACE':
                # Atualizar contador de linhas
                newlines = value.count('\n')
                if newlines > 0:
                    self.line += newlines
                continue  # Ignorar espaços em branco
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Caractere inesperado: {value} na linha {self.line}, coluna {current_column}')
            else:
                # Para outros tokens (operadores, símbolos, etc.)
                self.tokens.append(Token(kind, value, self.line, current_column))
        
        return self.tokens

def ler_arquivo(nome_arquivo):
    """Lê o conteúdo de um arquivo"""
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado!")
        return None
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return None

def main():
    """Função principal"""
    if len(sys.argv) != 2:
        print("Uso: python analisador_lexico.py <arquivo.py>")
        print("Exemplo: python analisador_lexico.py teste.py")
        sys.exit(1)
    
    nome_arquivo = sys.argv[1]
    
    # Verificar se o arquivo existe
    if not os.path.exists(nome_arquivo):
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado!")
        sys.exit(1)
    
    # Verificar se é um arquivo Python
    if not nome_arquivo.endswith('.py'):
        print("Aviso: O arquivo não tem extensão .py, mas continuando...")
    
    # Ler o conteúdo do arquivo
    codigo = ler_arquivo(nome_arquivo)
    if codigo is None:
        sys.exit(1)
    
    print(f"Analisando arquivo: {nome_arquivo}")
    print("=" * 60)
    
    # Criar e executar o lexer
    lexer = Lexer(codigo)
    
    try:
        tokens = lexer.tokenize()
        
        # Exibir resultados
        print(f"Total de tokens encontrados: {len(tokens)}")
        print("-" * 60)
        
        for i, token in enumerate(tokens, 1):
            print(f'{i:3d}. {token.type:12} {str(token.value):20} linha {token.line:2d}, coluna {token.column:2d}')
        
        # Estatísticas
        print("-" * 60)
        tipos_token = {}
        for token in tokens:
            tipos_token[token.type] = tipos_token.get(token.type, 0) + 1
        
        print("Estatísticas:")
        for tipo, quantidade in sorted(tipos_token.items()):
            print(f"  {tipo:12}: {quantidade:3d}")
            
    except RuntimeError as e:
        print(f"Erro durante análise léxica: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()