# Descrição
Este é um analisador léxico (lexer) desenvolvido em Python que realiza a análise léxica de código fonte Python, identificando e classificando tokens como palavras-chave, identificadores, números, strings, operadores e símbolos.

# Executar
python analisador_lexico.py teste.py

# Estrutura do Projeto
text
analisador_lexico/
│
├── analisador_lexico.py  # Código principal do analisador
├── teste.py              # Arquivo de exemplo para teste
└── README.md             # Este arquivo

# Salve o código em um arquivo analisador_lexico.py

# Tipos de Tokens Reconhecidos
Tipo do Token	  Exemplos	             Descrição
KEYWORD	          if, else, def, return	 Palavras reservadas do Python
IDENT	          x, soma, resultado     Identificadores (variáveis, funções)
NUMBER	          10, 3.14	             Números inteiros e decimais
STRING	          "hello", 'world'	     Strings literais
OPERATOR	      +, -, *, /, %	         Operadores aritméticos
ASSIGN	          =                      Operador de atribuição
COMPARISON	      ==, !=, <, >, <=, >=	 Operadores de comparação
BOOLEAN	          True, False	         Valores booleanos
LPAREN/RPAREN	  (, )	                 Parênteses
LBRACKET/RBRACKET [, ]	                 Colchetes
LBRACE/RBRACE	  {, }	                 Chaves
COMMA	          ,	                     Vírgula
COLON	          : 	                 Dois pontos
DOT	              .	                     Ponto
SEMI	          ;	                     Ponto e vírgula

Estrutura do Código
Classe Principal: 
# Lexer

Métodos Principais:
__init__(self, code)
Inicializa o analisador com o código fonte
Define as especificações dos tokens usando regex
Compila os padrões regex para eficiência

# tokenize(self)
Realiza a análise léxica propriamente dita
Itera sobre todas as correspondências regex
Classifica e armazena os tokens encontrados
Atualiza contadores de linha e coluna

Funções Auxiliares:
# ler_arquivo(nome_arquivo)
Lê o conteúdo do arquivo especificado
Trata erros de arquivo não encontrado
Retorna o conteúdo como string

# main()
Função principal do programa
Processa argumentos da linha de comando
Coordena todo o processo de análise
Exibe resultados e estatísticas

# Fluxo de Execução
Entrada: Recebe um arquivo .py como argumento
Leitura: Lê o conteúdo do arquivo
Análise: Realiza a análise léxica token por token
Classificação: Categoriza cada token encontrado
Saída: Exibe todos os tokens com suas informações
Estatísticas: Mostra resumo dos tokens encontrados