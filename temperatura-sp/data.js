const SITE_DATA = {
  "spec": {
    "baseC": 18.33,
    "baseF": 65.0,
    "slope": 21.1,
    "totalContratos": 72,
    "meses": [
      "Janeiro",
      "Fevereiro",
      "Março",
      "Abril",
      "Maio",
      "Junho",
      "Julho",
      "Agosto",
      "Setembro",
      "Outubro",
      "Novembro",
      "Dezembro"
    ],
    "strikes": [
      "-1.0σ",
      "-0.5σ",
      "+0.0σ",
      "+0.5σ",
      "+1.0σ",
      "+1.5σ"
    ],
    "anosClimatologia": "1981-2025 (45 anos)",
    "anosFinanceiro": "2003-2025 (excl. 2001-2002)"
  },
  "premiums": {
    "Janeiro": {
      "-1.0σ": {
        "premio": 146300.56,
        "prob": 0.872,
        "strikeCdd": 108.4,
        "taxaJuros": 13.543
      },
      "-0.5σ": {
        "premio": 111651.88,
        "prob": 0.739,
        "strikeCdd": 122.8,
        "taxaJuros": 13.543
      },
      "+0.0σ": {
        "premio": 79579.95,
        "prob": 0.611,
        "strikeCdd": 137.2,
        "taxaJuros": 13.543
      },
      "+0.5σ": {
        "premio": 55972.01,
        "prob": 0.259,
        "strikeCdd": 151.6,
        "taxaJuros": 13.543
      },
      "+1.0σ": {
        "premio": 36423.28,
        "prob": 0.263,
        "strikeCdd": 166.0,
        "taxaJuros": 13.543
      },
      "+1.5σ": {
        "premio": 16417.52,
        "prob": 0.215,
        "strikeCdd": 180.4,
        "taxaJuros": 13.543
      }
    },
    "Fevereiro": {
      "-1.0σ": {
        "premio": 157346.7,
        "prob": 0.913,
        "strikeCdd": 100.9,
        "taxaJuros": 13.577
      },
      "-0.5σ": {
        "premio": 117586.2,
        "prob": 0.826,
        "strikeCdd": 113.0,
        "taxaJuros": 13.577
      },
      "+0.0σ": {
        "premio": 84059.76,
        "prob": 0.609,
        "strikeCdd": 125.2,
        "taxaJuros": 13.577
      },
      "+0.5σ": {
        "premio": 64219.7,
        "prob": 0.351,
        "strikeCdd": 137.3,
        "taxaJuros": 13.577
      },
      "+1.0σ": {
        "premio": 49429.07,
        "prob": 0.173,
        "strikeCdd": 149.5,
        "taxaJuros": 13.577
      },
      "+1.5σ": {
        "premio": 38612.41,
        "prob": 0.13,
        "strikeCdd": 161.7,
        "taxaJuros": 13.577
      }
    },
    "Março": {
      "-1.0σ": {
        "premio": 163756.33,
        "prob": 0.957,
        "strikeCdd": 88.4,
        "taxaJuros": 13.62
      },
      "-0.5σ": {
        "premio": 116727.57,
        "prob": 0.825,
        "strikeCdd": 102.1,
        "taxaJuros": 13.62
      },
      "+0.0σ": {
        "premio": 80282.44,
        "prob": 0.612,
        "strikeCdd": 115.9,
        "taxaJuros": 13.62
      },
      "+0.5σ": {
        "premio": 53662.61,
        "prob": 0.349,
        "strikeCdd": 129.6,
        "taxaJuros": 13.62
      },
      "+1.0σ": {
        "premio": 32041.62,
        "prob": 0.215,
        "strikeCdd": 143.3,
        "taxaJuros": 13.62
      },
      "+1.5σ": {
        "premio": 17017.84,
        "prob": 0.177,
        "strikeCdd": 157.0,
        "taxaJuros": 13.62
      }
    },
    "Abril": {
      "-1.0σ": {
        "premio": 127392.68,
        "prob": 0.915,
        "strikeCdd": 41.4,
        "taxaJuros": 13.664
      },
      "-0.5σ": {
        "premio": 87425.47,
        "prob": 0.737,
        "strikeCdd": 55.2,
        "taxaJuros": 13.664
      },
      "+0.0σ": {
        "premio": 55365.84,
        "prob": 0.524,
        "strikeCdd": 69.0,
        "taxaJuros": 13.664
      },
      "+0.5σ": {
        "premio": 29046.39,
        "prob": 0.391,
        "strikeCdd": 82.8,
        "taxaJuros": 13.664
      },
      "+1.0σ": {
        "premio": 6573.57,
        "prob": 0.261,
        "strikeCdd": 96.5,
        "taxaJuros": 13.664
      },
      "+1.5σ": {
        "premio": 3626.36,
        "prob": 0.086,
        "strikeCdd": 110.3,
        "taxaJuros": 13.664
      }
    },
    "Maio": {
      "-1.0σ": {
        "premio": 116259.67,
        "prob": 1.0,
        "strikeCdd": 0.0,
        "taxaJuros": 13.705
      },
      "-0.5σ": {
        "premio": 77920.97,
        "prob": 0.738,
        "strikeCdd": 10.9,
        "taxaJuros": 13.705
      },
      "+0.0σ": {
        "premio": 47902.83,
        "prob": 0.307,
        "strikeCdd": 21.8,
        "taxaJuros": 13.705
      },
      "+0.5σ": {
        "premio": 29373.4,
        "prob": 0.216,
        "strikeCdd": 32.6,
        "taxaJuros": 13.705
      },
      "+1.0σ": {
        "premio": 14560.36,
        "prob": 0.176,
        "strikeCdd": 43.5,
        "taxaJuros": 13.705
      },
      "+1.5σ": {
        "premio": 6534.39,
        "prob": 0.085,
        "strikeCdd": 54.4,
        "taxaJuros": 13.705
      }
    },
    "Junho": {
      "-1.0σ": {
        "premio": 54424.74,
        "prob": 0.957,
        "strikeCdd": 0.0,
        "taxaJuros": 13.749
      },
      "-0.5σ": {
        "premio": 47016.43,
        "prob": 0.694,
        "strikeCdd": 2.7,
        "taxaJuros": 13.749
      },
      "+0.0σ": {
        "premio": 34401.24,
        "prob": 0.48,
        "strikeCdd": 8.0,
        "taxaJuros": 13.749
      },
      "+0.5σ": {
        "premio": 23900.73,
        "prob": 0.35,
        "strikeCdd": 13.4,
        "taxaJuros": 13.749
      },
      "+1.0σ": {
        "premio": 15282.64,
        "prob": 0.262,
        "strikeCdd": 18.7,
        "taxaJuros": 13.749
      },
      "+1.5σ": {
        "premio": 8618.1,
        "prob": 0.129,
        "strikeCdd": 24.0,
        "taxaJuros": 13.749
      }
    },
    "Julho": {
      "-1.0σ": {
        "premio": 52780.15,
        "prob": 0.957,
        "strikeCdd": 0.0,
        "taxaJuros": 13.794
      },
      "-0.5σ": {
        "premio": 45876.5,
        "prob": 0.869,
        "strikeCdd": 2.2,
        "taxaJuros": 13.794
      },
      "+0.0σ": {
        "premio": 32855.82,
        "prob": 0.478,
        "strikeCdd": 7.2,
        "taxaJuros": 13.794
      },
      "+0.5σ": {
        "premio": 24240.88,
        "prob": 0.217,
        "strikeCdd": 12.2,
        "taxaJuros": 13.794
      },
      "+1.0σ": {
        "premio": 19090.58,
        "prob": 0.131,
        "strikeCdd": 17.1,
        "taxaJuros": 13.794
      },
      "+1.5σ": {
        "premio": 15989.41,
        "prob": 0.088,
        "strikeCdd": 22.1,
        "taxaJuros": 13.794
      }
    },
    "Agosto": {
      "-1.0σ": {
        "premio": 126397.61,
        "prob": 1.0,
        "strikeCdd": 9.4,
        "taxaJuros": 13.685
      },
      "-0.5σ": {
        "premio": 90499.86,
        "prob": 0.697,
        "strikeCdd": 18.4,
        "taxaJuros": 13.685
      },
      "+0.0σ": {
        "premio": 58651.34,
        "prob": 0.609,
        "strikeCdd": 27.4,
        "taxaJuros": 13.685
      },
      "+0.5σ": {
        "premio": 33628.1,
        "prob": 0.347,
        "strikeCdd": 36.4,
        "taxaJuros": 13.685
      },
      "+1.0σ": {
        "premio": 18697.98,
        "prob": 0.307,
        "strikeCdd": 45.4,
        "taxaJuros": 13.685
      },
      "+1.5σ": {
        "premio": 7276.2,
        "prob": 0.171,
        "strikeCdd": 54.4,
        "taxaJuros": 13.685
      }
    },
    "Setembro": {
      "-1.0σ": {
        "premio": 398889.53,
        "prob": 1.0,
        "strikeCdd": 23.1,
        "taxaJuros": 13.62
      },
      "-0.5σ": {
        "premio": 302090.94,
        "prob": 0.826,
        "strikeCdd": 42.5,
        "taxaJuros": 13.62
      },
      "+0.0σ": {
        "premio": 210823.2,
        "prob": 0.608,
        "strikeCdd": 62.0,
        "taxaJuros": 13.62
      },
      "+0.5σ": {
        "premio": 128558.45,
        "prob": 0.568,
        "strikeCdd": 81.5,
        "taxaJuros": 13.62
      },
      "+1.0σ": {
        "premio": 61448.36,
        "prob": 0.348,
        "strikeCdd": 101.0,
        "taxaJuros": 13.62
      },
      "+1.5σ": {
        "premio": 31060.83,
        "prob": 0.173,
        "strikeCdd": 120.4,
        "taxaJuros": 13.62
      }
    },
    "Outubro": {
      "-1.0σ": {
        "premio": 400828.99,
        "prob": 0.955,
        "strikeCdd": 48.6,
        "taxaJuros": 13.548
      },
      "-0.5σ": {
        "premio": 296194.05,
        "prob": 0.821,
        "strikeCdd": 69.7,
        "taxaJuros": 13.548
      },
      "+0.0σ": {
        "premio": 201246.05,
        "prob": 0.68,
        "strikeCdd": 90.8,
        "taxaJuros": 13.548
      },
      "+0.5σ": {
        "premio": 121536.31,
        "prob": 0.453,
        "strikeCdd": 111.9,
        "taxaJuros": 13.548
      },
      "+1.0σ": {
        "premio": 47806.21,
        "prob": 0.318,
        "strikeCdd": 133.0,
        "taxaJuros": 13.548
      },
      "+1.5σ": {
        "premio": 5080.71,
        "prob": 0.091,
        "strikeCdd": 154.1,
        "taxaJuros": 13.548
      }
    },
    "Novembro": {
      "-1.0σ": {
        "premio": 167100.46,
        "prob": 0.908,
        "strikeCdd": 70.9,
        "taxaJuros": 13.538
      },
      "-0.5σ": {
        "premio": 109541.31,
        "prob": 0.774,
        "strikeCdd": 84.7,
        "taxaJuros": 13.538
      },
      "+0.0σ": {
        "premio": 61719.6,
        "prob": 0.589,
        "strikeCdd": 98.5,
        "taxaJuros": 13.538
      },
      "+0.5σ": {
        "premio": 26473.75,
        "prob": 0.367,
        "strikeCdd": 112.4,
        "taxaJuros": 13.538
      },
      "+1.0σ": {
        "premio": 6218.76,
        "prob": 0.138,
        "strikeCdd": 126.2,
        "taxaJuros": 13.538
      },
      "+1.5σ": {
        "premio": 3609.9,
        "prob": 0.091,
        "strikeCdd": 140.0,
        "taxaJuros": 13.538
      }
    },
    "Dezembro": {
      "-1.0σ": {
        "premio": 185447.28,
        "prob": 0.861,
        "strikeCdd": 93.9,
        "taxaJuros": 13.541
      },
      "-0.5σ": {
        "premio": 134612.17,
        "prob": 0.817,
        "strikeCdd": 110.4,
        "taxaJuros": 13.541
      },
      "+0.0σ": {
        "premio": 85168.92,
        "prob": 0.682,
        "strikeCdd": 127.0,
        "taxaJuros": 13.541
      },
      "+0.5σ": {
        "premio": 40534.23,
        "prob": 0.458,
        "strikeCdd": 143.5,
        "taxaJuros": 13.541
      },
      "+1.0σ": {
        "premio": 12531.14,
        "prob": 0.181,
        "strikeCdd": 160.1,
        "taxaJuros": 13.541
      },
      "+1.5σ": {
        "premio": 4312.53,
        "prob": 0.089,
        "strikeCdd": 176.7,
        "taxaJuros": 13.541
      }
    }
  },
  "climatologia": {
    "1.0": 137.2,
    "2.0": 125.2,
    "3.0": 115.9,
    "4.0": 69.0,
    "5.0": 21.8,
    "6.0": 8.0,
    "7.0": 7.2,
    "8.0": 27.4,
    "9.0": 62.0,
    "10.0": 90.8,
    "11.0": 98.5,
    "12.0": 127.0
  },
  "climatologiaStd": {
    "1.0": 28.8,
    "2.0": 24.3,
    "3.0": 27.5,
    "4.0": 27.6,
    "5.0": 21.7,
    "6.0": 10.7,
    "7.0": 9.9,
    "8.0": 18.0,
    "9.0": 38.9,
    "10.0": 42.2,
    "11.0": 27.6,
    "12.0": 33.1
  },
  "basisRisk": [
    {
      "strike_desvios": "-0.5σ",
      "N": 273,
      "TP": 63,
      "FP": 150,
      "FN": 6,
      "TN": 54,
      "sensibilidade": 0.913,
      "precisao": 0.296,
      "taxa_falso_negativo": 0.087
    },
    {
      "strike_desvios": "+0.0σ",
      "N": 273,
      "TP": 53,
      "FP": 101,
      "FN": 16,
      "TN": 103,
      "sensibilidade": 0.768,
      "precisao": 0.344,
      "taxa_falso_negativo": 0.232
    },
    {
      "strike_desvios": "+1.0σ",
      "N": 273,
      "TP": 26,
      "FP": 37,
      "FN": 43,
      "TN": 167,
      "sensibilidade": 0.377,
      "precisao": 0.413,
      "taxa_falso_negativo": 0.623
    }
  ],
  "semiVariancia": [
    {
      "strike_desvios": "-0.5σ",
      "custo_medio_sem_hedge_RS": 312308.0,
      "premio_RS": 134586.0,
      "SV_sem_hedge": 183432575199.0,
      "SV_com_hedge": 72464905299.0,
      "efetividade_pct": 60.5
    },
    {
      "strike_desvios": "+0.0σ",
      "custo_medio_sem_hedge_RS": 312308.0,
      "premio_RS": 90260.0,
      "SV_sem_hedge": 183432575199.0,
      "SV_com_hedge": 94346596449.0,
      "efetividade_pct": 48.6
    },
    {
      "strike_desvios": "+1.0σ",
      "custo_medio_sem_hedge_RS": 312308.0,
      "premio_RS": 28437.0,
      "SV_sem_hedge": 183432575199.0,
      "SV_com_hedge": 147115762310.0,
      "efetividade_pct": 19.8
    }
  ]
};
