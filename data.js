const SITE_DATA = {
  "spec": {
    "tick": 150,
    "cap": 60,
    "cargaRisco": 0.2,
    "cidades": [
      "Sorriso",
      "Sinop",
      "Lucas do Rio Verde"
    ],
    "meses": [
      "Setembro",
      "Outubro",
      "Novembro",
      "Dezembro",
      "Janeiro",
      "Fevereiro"
    ],
    "strikes": [
      "30%",
      "40%",
      "50%",
      "60%",
      "70%",
      "80%"
    ],
    "totalContratos": 108,
    "anosHistorico": "1990-2026",
    "safraAtiva": "2026/2027"
  },
  "premiums": {
    "Sorriso": {
      "Setembro": {
        "30%": {
          "premio": 218.97,
          "prob": 0.155,
          "strikeMm": 16.3,
          "taxaJuros": 13.676
        },
        "40%": {
          "premio": 389.17,
          "prob": 0.223,
          "strikeMm": 21.7,
          "taxaJuros": 13.676
        },
        "50%": {
          "premio": 609.03,
          "prob": 0.3,
          "strikeMm": 27.2,
          "taxaJuros": 13.676
        },
        "60%": {
          "premio": 880.84,
          "prob": 0.366,
          "strikeMm": 32.6,
          "taxaJuros": 13.676
        },
        "70%": {
          "premio": 1231.48,
          "prob": 0.434,
          "strikeMm": 38.0,
          "taxaJuros": 13.676
        },
        "80%": {
          "premio": 1640.65,
          "prob": 0.496,
          "strikeMm": 43.5,
          "taxaJuros": 13.676
        }
      },
      "Outubro": {
        "30%": {
          "premio": 0.91,
          "prob": 0.002,
          "strikeMm": 43.1,
          "taxaJuros": 13.631
        },
        "40%": {
          "premio": 53.09,
          "prob": 0.012,
          "strikeMm": 57.4,
          "taxaJuros": 13.631
        },
        "50%": {
          "premio": 152.63,
          "prob": 0.041,
          "strikeMm": 71.8,
          "taxaJuros": 13.631
        },
        "60%": {
          "premio": 304.74,
          "prob": 0.097,
          "strikeMm": 86.1,
          "taxaJuros": 13.631
        },
        "70%": {
          "premio": 609.3,
          "prob": 0.189,
          "strikeMm": 100.5,
          "taxaJuros": 13.631
        },
        "80%": {
          "premio": 1073.96,
          "prob": 0.3,
          "strikeMm": 114.8,
          "taxaJuros": 13.631
        }
      },
      "Novembro": {
        "30%": {
          "premio": 2.37,
          "prob": 0.003,
          "strikeMm": 61.7,
          "taxaJuros": 13.623
        },
        "40%": {
          "premio": 20.63,
          "prob": 0.016,
          "strikeMm": 82.3,
          "taxaJuros": 13.623
        },
        "50%": {
          "premio": 204.82,
          "prob": 0.053,
          "strikeMm": 102.9,
          "taxaJuros": 13.623
        },
        "60%": {
          "premio": 528.49,
          "prob": 0.111,
          "strikeMm": 123.4,
          "taxaJuros": 13.623
        },
        "70%": {
          "premio": 1120.63,
          "prob": 0.204,
          "strikeMm": 144.0,
          "taxaJuros": 13.623
        },
        "80%": {
          "premio": 1752.88,
          "prob": 0.315,
          "strikeMm": 164.6,
          "taxaJuros": 13.623
        }
      },
      "Dezembro": {
        "30%": {
          "premio": 0.93,
          "prob": 0.001,
          "strikeMm": 77.1,
          "taxaJuros": 13.616
        },
        "40%": {
          "premio": 10.21,
          "prob": 0.009,
          "strikeMm": 102.9,
          "taxaJuros": 13.616
        },
        "50%": {
          "premio": 85.06,
          "prob": 0.032,
          "strikeMm": 128.6,
          "taxaJuros": 13.616
        },
        "60%": {
          "premio": 437.26,
          "prob": 0.084,
          "strikeMm": 154.3,
          "taxaJuros": 13.616
        },
        "70%": {
          "premio": 1024.0,
          "prob": 0.17,
          "strikeMm": 180.0,
          "taxaJuros": 13.616
        },
        "80%": {
          "premio": 1643.38,
          "prob": 0.283,
          "strikeMm": 205.7,
          "taxaJuros": 13.616
        }
      },
      "Janeiro": {
        "30%": {
          "premio": 59.96,
          "prob": 0.012,
          "strikeMm": 80.1,
          "taxaJuros": 13.61
        },
        "40%": {
          "premio": 244.05,
          "prob": 0.039,
          "strikeMm": 106.8,
          "taxaJuros": 13.61
        },
        "50%": {
          "premio": 553.96,
          "prob": 0.089,
          "strikeMm": 133.5,
          "taxaJuros": 13.61
        },
        "60%": {
          "premio": 938.07,
          "prob": 0.163,
          "strikeMm": 160.2,
          "taxaJuros": 13.61
        },
        "70%": {
          "premio": 1438.3,
          "prob": 0.254,
          "strikeMm": 186.9,
          "taxaJuros": 13.61
        },
        "80%": {
          "premio": 2249.64,
          "prob": 0.353,
          "strikeMm": 213.6,
          "taxaJuros": 13.61
        }
      },
      "Fevereiro": {
        "30%": {
          "premio": 74.12,
          "prob": 0.006,
          "strikeMm": 82.0,
          "taxaJuros": 13.633
        },
        "40%": {
          "premio": 202.14,
          "prob": 0.023,
          "strikeMm": 109.4,
          "taxaJuros": 13.633
        },
        "50%": {
          "premio": 363.34,
          "prob": 0.062,
          "strikeMm": 136.7,
          "taxaJuros": 13.633
        },
        "60%": {
          "premio": 642.62,
          "prob": 0.127,
          "strikeMm": 164.1,
          "taxaJuros": 13.633
        },
        "70%": {
          "premio": 1174.06,
          "prob": 0.222,
          "strikeMm": 191.4,
          "taxaJuros": 13.633
        },
        "80%": {
          "premio": 1932.86,
          "prob": 0.326,
          "strikeMm": 218.8,
          "taxaJuros": 13.633
        }
      }
    },
    "Sinop": {
      "Setembro": {
        "30%": {
          "premio": 197.05,
          "prob": 0.135,
          "strikeMm": 17.8,
          "taxaJuros": 13.676
        },
        "40%": {
          "premio": 374.51,
          "prob": 0.206,
          "strikeMm": 23.7,
          "taxaJuros": 13.676
        },
        "50%": {
          "premio": 597.07,
          "prob": 0.284,
          "strikeMm": 29.6,
          "taxaJuros": 13.676
        },
        "60%": {
          "premio": 903.99,
          "prob": 0.355,
          "strikeMm": 35.5,
          "taxaJuros": 13.676
        },
        "70%": {
          "premio": 1269.03,
          "prob": 0.421,
          "strikeMm": 41.4,
          "taxaJuros": 13.676
        },
        "80%": {
          "premio": 1692.37,
          "prob": 0.485,
          "strikeMm": 47.3,
          "taxaJuros": 13.676
        }
      },
      "Outubro": {
        "30%": {
          "premio": 0.43,
          "prob": 0.001,
          "strikeMm": 44.3,
          "taxaJuros": 13.631
        },
        "40%": {
          "premio": 24.44,
          "prob": 0.008,
          "strikeMm": 59.1,
          "taxaJuros": 13.631
        },
        "50%": {
          "premio": 84.28,
          "prob": 0.032,
          "strikeMm": 73.9,
          "taxaJuros": 13.631
        },
        "60%": {
          "premio": 200.67,
          "prob": 0.084,
          "strikeMm": 88.7,
          "taxaJuros": 13.631
        },
        "70%": {
          "premio": 501.79,
          "prob": 0.171,
          "strikeMm": 103.4,
          "taxaJuros": 13.631
        },
        "80%": {
          "premio": 1078.42,
          "prob": 0.285,
          "strikeMm": 118.2,
          "taxaJuros": 13.631
        }
      },
      "Novembro": {
        "30%": {
          "premio": 2.79,
          "prob": 0.003,
          "strikeMm": 65.0,
          "taxaJuros": 13.623
        },
        "40%": {
          "premio": 33.27,
          "prob": 0.017,
          "strikeMm": 86.6,
          "taxaJuros": 13.623
        },
        "50%": {
          "premio": 194.05,
          "prob": 0.052,
          "strikeMm": 108.3,
          "taxaJuros": 13.623
        },
        "60%": {
          "premio": 559.77,
          "prob": 0.114,
          "strikeMm": 130.0,
          "taxaJuros": 13.623
        },
        "70%": {
          "premio": 1102.45,
          "prob": 0.204,
          "strikeMm": 151.6,
          "taxaJuros": 13.623
        },
        "80%": {
          "premio": 1751.94,
          "prob": 0.31,
          "strikeMm": 173.3,
          "taxaJuros": 13.623
        }
      },
      "Dezembro": {
        "30%": {
          "premio": 0.41,
          "prob": 0.001,
          "strikeMm": 79.1,
          "taxaJuros": 13.616
        },
        "40%": {
          "premio": 8.52,
          "prob": 0.008,
          "strikeMm": 105.4,
          "taxaJuros": 13.616
        },
        "50%": {
          "premio": 123.29,
          "prob": 0.031,
          "strikeMm": 131.8,
          "taxaJuros": 13.616
        },
        "60%": {
          "premio": 401.21,
          "prob": 0.082,
          "strikeMm": 158.1,
          "taxaJuros": 13.616
        },
        "70%": {
          "premio": 935.71,
          "prob": 0.172,
          "strikeMm": 184.5,
          "taxaJuros": 13.616
        },
        "80%": {
          "premio": 1635.82,
          "prob": 0.28,
          "strikeMm": 210.8,
          "taxaJuros": 13.616
        }
      },
      "Janeiro": {
        "30%": {
          "premio": 10.45,
          "prob": 0.009,
          "strikeMm": 80.2,
          "taxaJuros": 13.61
        },
        "40%": {
          "premio": 113.25,
          "prob": 0.032,
          "strikeMm": 107.0,
          "taxaJuros": 13.61
        },
        "50%": {
          "premio": 442.75,
          "prob": 0.075,
          "strikeMm": 133.7,
          "taxaJuros": 13.61
        },
        "60%": {
          "premio": 962.23,
          "prob": 0.143,
          "strikeMm": 160.4,
          "taxaJuros": 13.61
        },
        "70%": {
          "premio": 1558.25,
          "prob": 0.24,
          "strikeMm": 187.2,
          "taxaJuros": 13.61
        },
        "80%": {
          "premio": 2229.32,
          "prob": 0.342,
          "strikeMm": 213.9,
          "taxaJuros": 13.61
        }
      },
      "Fevereiro": {
        "30%": {
          "premio": 2.13,
          "prob": 0.002,
          "strikeMm": 82.7,
          "taxaJuros": 13.633
        },
        "40%": {
          "premio": 76.23,
          "prob": 0.013,
          "strikeMm": 110.2,
          "taxaJuros": 13.633
        },
        "50%": {
          "premio": 197.08,
          "prob": 0.042,
          "strikeMm": 137.8,
          "taxaJuros": 13.633
        },
        "60%": {
          "premio": 463.87,
          "prob": 0.101,
          "strikeMm": 165.3,
          "taxaJuros": 13.633
        },
        "70%": {
          "premio": 1088.18,
          "prob": 0.187,
          "strikeMm": 192.9,
          "taxaJuros": 13.633
        },
        "80%": {
          "premio": 1960.42,
          "prob": 0.302,
          "strikeMm": 220.5,
          "taxaJuros": 13.633
        }
      }
    },
    "Lucas do Rio Verde": {
      "Setembro": {
        "30%": {
          "premio": 229.2,
          "prob": 0.156,
          "strikeMm": 16.6,
          "taxaJuros": 13.676
        },
        "40%": {
          "premio": 411.3,
          "prob": 0.228,
          "strikeMm": 22.1,
          "taxaJuros": 13.676
        },
        "50%": {
          "premio": 642.46,
          "prob": 0.301,
          "strikeMm": 27.7,
          "taxaJuros": 13.676
        },
        "60%": {
          "premio": 907.64,
          "prob": 0.37,
          "strikeMm": 33.2,
          "taxaJuros": 13.676
        },
        "70%": {
          "premio": 1271.68,
          "prob": 0.437,
          "strikeMm": 38.7,
          "taxaJuros": 13.676
        },
        "80%": {
          "premio": 1698.24,
          "prob": 0.494,
          "strikeMm": 44.3,
          "taxaJuros": 13.676
        }
      },
      "Outubro": {
        "30%": {
          "premio": 14.68,
          "prob": 0.004,
          "strikeMm": 43.3,
          "taxaJuros": 13.631
        },
        "40%": {
          "premio": 90.02,
          "prob": 0.019,
          "strikeMm": 57.8,
          "taxaJuros": 13.631
        },
        "50%": {
          "premio": 203.95,
          "prob": 0.054,
          "strikeMm": 72.2,
          "taxaJuros": 13.631
        },
        "60%": {
          "premio": 393.63,
          "prob": 0.122,
          "strikeMm": 86.7,
          "taxaJuros": 13.631
        },
        "70%": {
          "premio": 752.61,
          "prob": 0.209,
          "strikeMm": 101.1,
          "taxaJuros": 13.631
        },
        "80%": {
          "premio": 1304.93,
          "prob": 0.315,
          "strikeMm": 115.6,
          "taxaJuros": 13.631
        }
      },
      "Novembro": {
        "30%": {
          "premio": 1.05,
          "prob": 0.002,
          "strikeMm": 61.5,
          "taxaJuros": 13.623
        },
        "40%": {
          "premio": 18.39,
          "prob": 0.009,
          "strikeMm": 82.0,
          "taxaJuros": 13.623
        },
        "50%": {
          "premio": 142.31,
          "prob": 0.036,
          "strikeMm": 102.6,
          "taxaJuros": 13.623
        },
        "60%": {
          "premio": 383.62,
          "prob": 0.091,
          "strikeMm": 123.1,
          "taxaJuros": 13.623
        },
        "70%": {
          "premio": 890.24,
          "prob": 0.179,
          "strikeMm": 143.6,
          "taxaJuros": 13.623
        },
        "80%": {
          "premio": 1579.87,
          "prob": 0.293,
          "strikeMm": 164.1,
          "taxaJuros": 13.623
        }
      },
      "Dezembro": {
        "30%": {
          "premio": 2.82,
          "prob": 0.003,
          "strikeMm": 77.9,
          "taxaJuros": 13.616
        },
        "40%": {
          "premio": 18.88,
          "prob": 0.015,
          "strikeMm": 103.8,
          "taxaJuros": 13.616
        },
        "50%": {
          "premio": 126.48,
          "prob": 0.045,
          "strikeMm": 129.8,
          "taxaJuros": 13.616
        },
        "60%": {
          "premio": 563.22,
          "prob": 0.109,
          "strikeMm": 155.7,
          "taxaJuros": 13.616
        },
        "70%": {
          "premio": 1265.25,
          "prob": 0.198,
          "strikeMm": 181.7,
          "taxaJuros": 13.616
        },
        "80%": {
          "premio": 1934.05,
          "prob": 0.305,
          "strikeMm": 207.7,
          "taxaJuros": 13.616
        }
      },
      "Janeiro": {
        "30%": {
          "premio": 16.16,
          "prob": 0.013,
          "strikeMm": 84.0,
          "taxaJuros": 13.61
        },
        "40%": {
          "premio": 227.63,
          "prob": 0.042,
          "strikeMm": 112.0,
          "taxaJuros": 13.61
        },
        "50%": {
          "premio": 646.08,
          "prob": 0.094,
          "strikeMm": 140.0,
          "taxaJuros": 13.61
        },
        "60%": {
          "premio": 1085.36,
          "prob": 0.167,
          "strikeMm": 168.0,
          "taxaJuros": 13.61
        },
        "70%": {
          "premio": 1639.38,
          "prob": 0.258,
          "strikeMm": 196.0,
          "taxaJuros": 13.61
        },
        "80%": {
          "premio": 2367.71,
          "prob": 0.355,
          "strikeMm": 224.0,
          "taxaJuros": 13.61
        }
      },
      "Fevereiro": {
        "30%": {
          "premio": 24.96,
          "prob": 0.003,
          "strikeMm": 84.3,
          "taxaJuros": 13.633
        },
        "40%": {
          "premio": 124.1,
          "prob": 0.017,
          "strikeMm": 112.4,
          "taxaJuros": 13.633
        },
        "50%": {
          "premio": 317.38,
          "prob": 0.051,
          "strikeMm": 140.5,
          "taxaJuros": 13.633
        },
        "60%": {
          "premio": 591.71,
          "prob": 0.113,
          "strikeMm": 168.5,
          "taxaJuros": 13.633
        },
        "70%": {
          "premio": 1080.82,
          "prob": 0.204,
          "strikeMm": 196.6,
          "taxaJuros": 13.633
        },
        "80%": {
          "premio": 1841.0,
          "prob": 0.311,
          "strikeMm": 224.7,
          "taxaJuros": 13.633
        }
      }
    }
  },
  "climatologia": {
    "Sorriso": {
      "Setembro": 54.3,
      "Outubro": 143.5,
      "Novembro": 205.7,
      "Dezembro": 257.2,
      "Janeiro": 266.9,
      "Fevereiro": 273.5
    },
    "Sinop": {
      "Setembro": 59.2,
      "Outubro": 147.8,
      "Novembro": 216.6,
      "Dezembro": 263.5,
      "Janeiro": 267.4,
      "Fevereiro": 275.6
    },
    "Lucas do Rio Verde": {
      "Setembro": 55.3,
      "Outubro": 144.4,
      "Novembro": 205.1,
      "Dezembro": 259.6,
      "Janeiro": 280.0,
      "Fevereiro": 280.9
    }
  },
  "basisRisk": [
    {
      "strike": "30%",
      "N": 105,
      "TP": 13,
      "FP": 8,
      "FN": 36,
      "TN": 48,
      "sensibilidade": 0.2653061224489796,
      "precisao": 0.6190476190476191,
      "taxa_falso_negativo": 0.7346938775510204
    },
    {
      "strike": "40%",
      "N": 105,
      "TP": 16,
      "FP": 8,
      "FN": 33,
      "TN": 48,
      "sensibilidade": 0.3265306122448979,
      "precisao": 0.6666666666666666,
      "taxa_falso_negativo": 0.673469387755102
    },
    {
      "strike": "50%",
      "N": 105,
      "TP": 19,
      "FP": 12,
      "FN": 30,
      "TN": 44,
      "sensibilidade": 0.3877551020408163,
      "precisao": 0.6129032258064516,
      "taxa_falso_negativo": 0.6122448979591837
    },
    {
      "strike": "60%",
      "N": 105,
      "TP": 29,
      "FP": 17,
      "FN": 20,
      "TN": 39,
      "sensibilidade": 0.5918367346938775,
      "precisao": 0.6304347826086957,
      "taxa_falso_negativo": 0.4081632653061224
    },
    {
      "strike": "70%",
      "N": 105,
      "TP": 35,
      "FP": 27,
      "FN": 14,
      "TN": 29,
      "sensibilidade": 0.7142857142857143,
      "precisao": 0.5645161290322581,
      "taxa_falso_negativo": 0.2857142857142857
    },
    {
      "strike": "80%",
      "N": 105,
      "TP": 39,
      "FP": 32,
      "FN": 10,
      "TN": 24,
      "sensibilidade": 0.7959183673469388,
      "precisao": 0.5492957746478874,
      "taxa_falso_negativo": 0.2040816326530612
    }
  ],
  "semiVariancia": [
    {
      "strike": "30%",
      "n": 105,
      "SV_sem_hedge": 45934.8,
      "SV_com_hedge_critico": 60380.2,
      "SV_com_hedge_temporada": 133282.0,
      "efetividade_critico_pct": -31.4,
      "efetividade_temporada_pct": -190.2,
      "custo_premio_critico_pct_payoff_max": 0.5,
      "custo_premio_temporada_pct_payoff_max": 0.7
    },
    {
      "strike": "50%",
      "n": 105,
      "SV_sem_hedge": 45934.8,
      "SV_com_hedge_critico": 869649.2,
      "SV_com_hedge_temporada": 2278535.6,
      "efetividade_critico_pct": -1793.2,
      "efetividade_temporada_pct": -4860.4,
      "custo_premio_critico_pct_payoff_max": 6.2,
      "custo_premio_temporada_pct_payoff_max": 4.3
    },
    {
      "strike": "80%",
      "n": 105,
      "SV_sem_hedge": 45934.8,
      "SV_com_hedge_critico": 7393699.8,
      "SV_com_hedge_temporada": 30382535.4,
      "efetividade_critico_pct": -15996.1,
      "efetividade_temporada_pct": -66042.7,
      "custo_premio_critico_pct_payoff_max": 23.5,
      "custo_premio_temporada_pct_payoff_max": 19.6
    }
  ],
  "hedgeOtimo": [
    {
      "strike": "30%",
      "janela": "critico",
      "h_star_contratos_por_ha": -0.0492,
      "efetividade_h_star_pct": -2.5
    },
    {
      "strike": "30%",
      "janela": "temporada",
      "h_star_contratos_por_ha": -0.0098,
      "efetividade_h_star_pct": -0.5
    },
    {
      "strike": "50%",
      "janela": "critico",
      "h_star_contratos_por_ha": -0.0131,
      "efetividade_h_star_pct": -6.1
    },
    {
      "strike": "50%",
      "janela": "temporada",
      "h_star_contratos_por_ha": -0.0082,
      "efetividade_h_star_pct": -5.2
    },
    {
      "strike": "80%",
      "janela": "critico",
      "h_star_contratos_por_ha": -0.0094,
      "efetividade_h_star_pct": -10.9
    },
    {
      "strike": "80%",
      "janela": "temporada",
      "h_star_contratos_por_ha": -0.0019,
      "efetividade_h_star_pct": -2.3
    }
  ]
};
