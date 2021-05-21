SemanticCube = {
      '*': {
        'CTE_INT': {
          'CTE_INT': 'CTE_INT',
          'CTE_FLOAT': 'CTE_FLOAT',
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_FLOAT': {
          'CTE_INT': 'CTE_FLOAT',
          'CTE_FLOAT': 'CTE_FLOAT',
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_BOOL': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_STRING': {
          'CTE_INT': 'CTE_STRING',
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_FILE': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        }
      },
      '/': {
        'CTE_INT': {
          'CTE_INT': 'CTE_INT',
          'CTE_FLOAT': 'CTE_FLOAT',
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_FLOAT': {
          'CTE_INT': 'CTE_FLOAT',
          'CTE_FLOAT': 'CTE_FLOAT',
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_BOOL': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_STRING': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_FILE': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        }
      },
      '+': {
        'CTE_INT': {
          'CTE_INT': 'CTE_INT',
          'CTE_FLOAT': 'CTE_FLOAT',
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_FLOAT': {
          'CTE_INT': 'CTE_FLOAT',
          'CTE_FLOAT': 'CTE_FLOAT',
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_BOOL': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_STRING': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': 'CTE_STRING',
          'CTE_FILE': False
        },
        'CTE_FILE': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': 'CTE_FILE',
          'CTE_FILE': 'CTE_FILE'
        }
      },
      '-': {
        'CTE_INT': {
          'CTE_INT': 'CTE_INT',
          'CTE_FLOAT': 'CTE_FLOAT',
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_FLOAT': {
          'CTE_INT': 'CTE_FLOAT',
          'CTE_FLOAT': 'CTE_FLOAT',
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_BOOL': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_STRING': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': 'CTE_STRING',
          'CTE_FILE': False
        },
        'CTE_FILE': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': 'CTE_FILE',
          'CTE_FILE': False
        }
      },
      'comp': {
        'CTE_INT': {
          'CTE_INT': 'CTE_BOOL',
          'CTE_FLOAT': 'CTE_BOOL',
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_FLOAT': {
          'CTE_INT': 'CTE_BOOL',
          'CTE_FLOAT': 'CTE_BOOL',
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_BOOL': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': 'CTE_BOOL',
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_STRING': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': 'CTE_BOOL',
          'CTE_FILE': False
        },
        'CTE_FILE': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': 'CTE_BOOL',
          'CTE_FILE': False
        }
      },
      'not': {
        'CTE_INT': False,
        'CTE_FLOAT': False,
        'CTE_BOOL': 'CTE_BOOL',
        'CTE_STRING': False,
        'CTE_FILE': False
      },
      'compao': {
        'CTE_INT': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_FLOAT': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_BOOL': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': 'CTE_BOOL',
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_STRING': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        },
        'CTE_FILE': {
          'CTE_INT': False,
          'CTE_FLOAT': False,
          'CTE_BOOL': False,
          'CTE_STRING': False,
          'CTE_FILE': False
        }
      }
    }