# pyUmschrift
import array
from sys import byteorder
# from .constants import *
# from .dicts import *
from enum import IntEnum, IntFlag, auto


class Format(IntEnum):
    COMMON_D = auto()  # dict element common for all scenarios
    # relating to the Umschrift_TTn v3.0 font (https://wwwuser.gwdg.de/~lingaeg/lingaeg-stylesheet.htm)
    UMSCHRIFT_TTN = auto()
    # relating to the Transliteration font (CCER), downloadable from the link above
    TRANSLITERATION = auto()
    TRLIT_CG_TIMES = auto()  # relating to the pre-2023 version of the Trlit_CG Times font
    # relating to the 2023 version of the Trlit_CG Times font (https://dmd.wepwawet.nl/fonts.htm https://oeb.griffith.ox.ac.uk/fonts.aspx)
    TRLIT_CG_TIMES_2023 = auto()
    UNICODE = auto()  # (relating to the Unicode encoding of Egyptological transliteration/transcription as per http://hdl.handle.net/21.11101/0000-0000-9E1A-2 )


class UmExport(IntFlag):
    K_WITH_DOT = auto()  # uses ḳ and Ḳ for q and Q
    J_FOR_YOD = auto()  # uses j and J for ꞽ and Ꞽ
    JJ_FOR_DOUBLE_YOD = auto()  # uses jj and Jj for y and Y
    REPLACE_I_WITH_DIAERESIS = auto()  # uses y and Y for ï and Ï
    Z_FOR_S_AND_S_FOR_S_ACUTE = auto()  # uses s, S and ś, Ś for z, Z and s, S


class UmImport(IntFlag):
    S_FOR_Z = auto()  # interprets s and S as z and Z


class UmFilter(IntFlag):

    MORPH = auto()  # removes morphological markers . : ·
    SUFF_PRON = auto()  # removes suffix pronoun separators ⸗
    BRACKETS = auto()  # removes brackets ⸢ ⸣ ⟨ ⟩ ( ) [ ] < > { } |
    PUNCT = auto()  # removes punctuation ? ! " , .
    # removes  all of the above
    CLEAN = MORPH | SUFF_PRON | BRACKETS | PUNCT
    REPLACE_Z = auto()  # uses s for z and S for Z
    REPLACE_I_WITH_DIAERESIS = auto()  # uses y for ï
    REPLACE_INVERTED_BREVES = auto()  # uses ꞽ for i̯, w for u̯
    REPLACE_UNCERTAIN_CONSONANT = auto()  # uses ꜣ for ꜥ
    REPLACE_ALL = REPLACE_I_WITH_DIAERESIS | REPLACE_INVERTED_BREVES | \
        REPLACE_UNCERTAIN_CONSONANT | REPLACE_Z  # replaces all of the above
    DIGITS = auto()  # removes all digits
    FACULTATIVE = auto()  # removes parentheses and all signs enclosed in parentheses
    LOWER = auto()  # converts all transliteration/transcription to lower case
    HYPHENS = auto()  # replaces all hyphens with spaces


ASC_SPACE = 32

ASC_SUFFIX_PRONOMEN_SEPARATOR = 61
ASC_EXCLAMATION_MARK = 33
ASC_QUOTE = 34
ASC_NUMBER = 35
ASC_DOLLAR = 36
ASC_PERCENT = 37
ASC_AMP = 38
ASC_APOSTROPHE = 39
ASC_LEFT_PARENTHESIS = 40
ASC_RIGHT_PARENTHESIS = 41
ASC_ASTERISK = 42
ASC_PLUS = 43
ASC_SLASH = 47
ASC_EQUALS = 0x003D
ASC_SECTION = 0x00A7
ASC_LOW_LINE = 0x005F
ASC_AT = 0x0040
ASC_AMPERSAND = 0x0026
ASC_CIRCUMFLEX_ACCENT = 0x005E
ASC_YEN = 0x00A5
ASC_DOT = 0x002E
ASC_COMMA = 44
ASC_QUESTION_MARK = 63
ASC_SEMICOLON = 0x003B
ASC_COLON = 0x003A
ASC_LEFT_PARENTHESIS = 0x0028
ASC_RIGHT_PARENTHESIS = 0x0029
ASC_LEFT_SQUARE_BRACKET = 0x005B
ASC_RIGHT_SQUARE_BRACKET = 0x005D
ASC_LESS_THAN_SIGN = 0x003C
ASC_GREATER_THAN_SIGN = 0x003E
ASC_LEFT_CURLY_BRACKET = 0x007B
ASC_RIGHT_CURLY_BRACKET = 0x007D
ASC_VERTICAL_LINE = 0x007C
ASC_ZERO = 48
ASC_NINE = 57
ASC_SOLIDUS = 0x002F
ASC_REVERSE_SOLIDUS = 0x005C
ASC_HYPHEN_MINUS = 0x002D
ASC_TILDE = 126
ASC_GRAVIS = 0x0060

ASC_a = 97
ASC_b = 98
ASC_c = 99
ASC_d = 100
ASC_e = 101
ASC_f = 102
ASC_g = 103
ASC_h = 104
ASC_i = 105
ASC_j = 106
ASC_k = 107
ASC_l = 108
ASC_m = 109
ASC_n = 110
ASC_o = 111
ASC_p = 112
ASC_q = 113
ASC_r = 114
ASC_s = 115
ASC_t = 116
ASC_u = 117
ASC_v = 118
ASC_w = 119
ASC_x = 120
ASC_y = 121
ASC_z = 122
ASC_A = 65
ASC_B = 66
ASC_C = 67
ASC_D = 68
ASC_E = 69
ASC_F = 70
ASC_G = 71
ASC_H = 72
ASC_I = 73
ASC_J = 74
ASC_K = 75
ASC_L = 76
ASC_M = 77
ASC_N = 78
ASC_O = 79
ASC_P = 80
ASC_Q = 81
ASC_R = 82
ASC_S = 83
ASC_T = 84
ASC_U = 85
ASC_V = 86
ASC_W = 87
ASC_X = 88
ASC_Y = 89
ASC_Z = 90

PSEUDO_SMALL_ALEPH = 0xF101
PSEUDO_CAPITAL_ALEPH = 0xF100
PSEUDO_SMALL_YOD = 0xF103
PSEUDO_CAPITAL_YOD = 0xF102
PSEUDO_e = 0xF105
PSEUDO_E = 0xF104
PSEUDO_y = 0xF107
PSEUDO_Y = 0xF106
PSEUDO_i_WITH_DIAERESIS = 0xF109
PSEUDO_I_WITH_DIAERESIS = 0xF108
PSEUDO_i_WITH_INVERTED_BREVE = 0xF10B
PSEUDO_I_WITH_INVERTED_BREVE = 0xF10A
PSEUDO_RIGHT_HALF_RING = 0xF10C

PSEUDO_SMALL_AIN = 0xF10F
PSEUDO_CAPITAL_AIN = 0xF10E

PSEUDO_w = 0xF113
PSEUDO_W = 0xF112
PSEUDO_u_WITH_INVERTED_BREVE = 0xF115
PSEUDO_U_WITH_INVERTED_BREVE = 0xF114
PSEUDO_b = 0xF117
PSEUDO_B = 0xF116
PSEUDO_p = 0xF119
PSEUDO_P = 0xF118
PSEUDO_f = 0xF11B
PSEUDO_F = 0xF11A
PSEUDO_m = 0xF11D
PSEUDO_M = 0xF11C
PSEUDO_n = 0xF11F
PSEUDO_N = 0xF11E
PSEUDO_r = 0xF121
PSEUDO_R = 0xF120
PSEUDO_l = 0xF123
PSEUDO_L = 0xF122
PSEUDO_h = 0xF125
PSEUDO_H = 0xF124
PSEUDO_h_WITH_DOT = 0xF127
PSEUDO_H_WITH_DOT = 0xF126
PSEUDO_h_WITH_BREVE = 0xF129
PSEUDO_H_WITH_BREVE = 0xF128
PSEUDO_h_WITH_CURCUMFLEX = 0xF12B
PSEUDO_H_WITH_CURCUMFLEX = 0xF12A
PSEUDO_h_WITH_LINE = 0xF12D
PSEUDO_H_WITH_LINE = 0xF12C
PSEUDO_z = 0xF12F
PSEUDO_Z = 0xF12E
PSEUDO_s = 0xF131
PSEUDO_S = 0xF130
PSEUDO_s_WITH_CARON = 0xF133
PSEUDO_S_WITH_CARON = 0xF132
PSEUDO_q = 0xF135
PSEUDO_Q = 0xF134
PSEUDO_k = 0xF137
PSEUDO_K = 0xF136
PSEUDO_g = 0xF139
PSEUDO_G = 0xF138
PSEUDO_t = 0xF13B
PSEUDO_T = 0xF13A
PSEUDO_t_WITH_CURCUMFLEX = 0xF13D
PSEUDO_T_WITH_CURCUMFLEX = 0xF13C
PSEUDO_t_WITH_LINE = 0xF13F
PSEUDO_T_WITH_LINE = 0xF13E
PSEUDO_d = 0xF141
PSEUDO_D = 0xF140
PSEUDO_d_WITH_LINE = 0xF143
PSEUDO_D_WITH_LINE = 0xF142

PSEUDO_DOT = 0xF020
PSEUDO_MIDDLE_DOT = 0xF021
PSEUDO_COLON = 0xF022
PSEUDO_SUFFIX_PRONOMEN_SEPARATOR = 0xF023
PSEUDO_TOP_LEFT_HALF_BRACKET = 0xF0A0
PSEUDO_TOP_RIGHT_HALF_BRACKET = 0xF0A1
PSEUDO_LEFT_ANGLE_BRACKET = 0xF0A2
PSEUDO_RIGHT_ANGLE_BRACKET = 0xF0A3

UN_SMALL_ALEPH = 0xA723
UN_CAPITAL_ALEPH = 0xA722
UN_SMALL_YOD = 0xA7BD
UN_CAPITAL_YOD = 0xA7BC
UN_i_WITH_DIAERESIS = 0x00EF
UN_I_WITH_DIAERESIS = 0x00CF
UN_i_WITH_INVERTED_BREVE = 0xEC44  # to be replaced with i + 0x032F
UN_I_WITH_INVERTED_BREVE = 0xEC83  # to be replaced with I + 0x032F
UN_SMALL_AIN = 0xA725
UN_CAPITAL_AIN = 0xA724
UN_u_WITH_INVERTED_BREVE = 0xEC45  # to be replaced with u + 0x032F
UN_U_WITH_INVERTED_BREVE = 0xEC84  # to be replaced with U + 0x032F
UN_h_WITH_DOT = 0x1E25
UN_H_WITH_DOT = 0x1E24
UN_h_WITH_BREVE = 0x1E2B
UN_H_WITH_BREVE = 0x1E2A
UN_h_WITH_LINE = 0x1E96
UN_H_WITH_LINE = 0xEC40  # to be replaced with H + 0x0331
UN_s_WITH_ACUTE = 0x015B
UN_S_WITH_ACUTE = 0x015A
UN_s_WITH_CARON = 0x0161
UN_S_WITH_CARON = 0x0160

UN_k_WITH_DOT = 0x1E33
UN_K_WITH_DOT = 0x1E32
UN_t_WITH_LINE = 0x1E6F
UN_T_WITH_LINE = 0x1E6E
UN_d_WITH_LINE = 0x1E0F
UN_D_WITH_LINE = 0x1E0E

UN_RIGHT_HALF_RING = 0x02BE
UN_h_WITH_CURCUMFLEX = 0xEC47  # to be replaced with h + 0x032D
UN_H_WITH_CURCUMFLEX = 0xEC48  # to be replaced with H + 0x032D
UN_t_WITH_CURCUMFLEX = 0x1E71
UN_T_WITH_CURCUMFLEX = 0x1E70
UN_c_WITH_CARON = 0x010D
UN_C_WITH_CARON = 0x010C
UN_t_WITH_DOT = 0x1E6D
UN_T_WITH_DOT = 0x1E6C

UN_SMALL_DOTLESS_I = 0x0131
UN_COMBINING_MACRON_BELOW = 0x0331
UN_COMBINING_CIRCUMFLEX_BELOW = 0x032D
UN_COMBINING_INVERTED_BREVE = 0x032F
UN_COMBINING_RIGHT_HALF_RING_ABOVE = 0x0357
UN_COMBINING_CYRILLIC_PSILI_PNEUMATA = 0x0486
UN_COMBINING_DOT_BELOW = 0x0323
UN_TOP_LEFT_HALF_BRACKET = 0x2E22
UN_TOP_RIGHT_HALF_BRACKET = 0x2E23
UN_LEFT_ANGLE_BRACKET = 0x27E8
UN_RIGHT_ANGLE_BRACKET = 0x27E9
UN_SUFFIX_PRONOMEN_SEPARATOR = 0x2E17
UN_MIDDLE_DOT = 0x00B7
UN_HYPHEN = 0x2010
UN_HORIZONTAL_BAR = 0x2015
UN_MINUS_SIGN = 0x2212
UN_NO_BREAK_SPACE = 0x00A0
UN_FEMININE_ORDINAL_INDICATOR = 0x00AA
UN_LEFT_POINTING_DOUBLE_ANGLE_QUOTATION_MARK = 0x00AB
UN_RIGHT_POINTING_DOUBLE_ANGLE_QUOTATION_MARK = 0x00BB
UN_NOT_SIGN = 0x00AC
UN_SOFT_HYPHEN = 0x00AD
UN_PILCROW_SIGN = 0x00B6
UN_CEDILLA = 0x00B8
UN_INVERTED_QUESTION_MARK = 0x00BF
UN_MULTIPLICATION_SIGN = 0x00D7
UN_LATIN_SMALL_LETTER_SHARP_S = 0x00DF
UN_DIVISION_SIGN = 0x00F7
UN_LATIN_SMALL_LETTER_O_WITH_STROKE = 0x00F
UN_LATIN_SMALL_LETTER_THORN = 0x00FE
UN_EN_QUAD = 0x2000
UN_NOMINAL_DIGIT_SHAPES = 0x206F

UN_DECODE_BEFORE_COMBINING_MACRON = {ASC_H: PSEUDO_H_WITH_LINE,
                                     ASC_h: PSEUDO_h_WITH_LINE,
                                     ASC_d: PSEUDO_d_WITH_LINE,
                                     ASC_D: PSEUDO_D_WITH_LINE,
                                     ASC_t: PSEUDO_t_WITH_LINE,
                                     ASC_T: PSEUDO_T_WITH_LINE}
UN_DECODE_BEFORE_COMBINING_CIRCUMFLEX = {ASC_H: PSEUDO_H_WITH_CURCUMFLEX,
                                         ASC_h: PSEUDO_h_WITH_CURCUMFLEX,
                                         ASC_t: PSEUDO_t_WITH_CURCUMFLEX,
                                         ASC_T: PSEUDO_T_WITH_CURCUMFLEX}
UN_DECODE_BEFORE_COMBINING_INVERTED_BREVE = {ASC_i: PSEUDO_i_WITH_INVERTED_BREVE,
                                             ASC_I: PSEUDO_I_WITH_INVERTED_BREVE,
                                             ASC_u: PSEUDO_u_WITH_INVERTED_BREVE,
                                             ASC_U: PSEUDO_U_WITH_INVERTED_BREVE}
UN_DECODE_BEFORE_COMBINING_DOT_BELOW = {ASC_k: PSEUDO_q,
                                        ASC_K: PSEUDO_Q,
                                        ASC_h: PSEUDO_h_WITH_DOT,
                                        ASC_H: PSEUDO_H_WITH_DOT,
                                        ASC_t: PSEUDO_d,
                                        ASC_T: PSEUDO_D,
                                        UN_c_WITH_CARON: PSEUDO_d_WITH_LINE,
                                        UN_C_WITH_CARON: PSEUDO_D_WITH_LINE}
UN_DECODE_BEFORE_COMBINING_HALF_RING_ABOVE = {ASC_i: PSEUDO_SMALL_YOD,
                                              UN_SMALL_DOTLESS_I: PSEUDO_SMALL_YOD,
                                              ASC_I: PSEUDO_CAPITAL_YOD}
IMPORT_DICT = {Format.UMSCHRIFT_TTN: {ASC_Y: PSEUDO_Y, ASC_L: PSEUDO_L, 0x00C7: PSEUDO_T_WITH_LINE, 0x008D: PSEUDO_SMALL_ALEPH, 0x0160: ASC_TILDE, 0x03BC: PSEUDO_E, 0x00CB: ASC_PLUS, 0x00F4: PSEUDO_d, 0xa6: PSEUDO_SMALL_YOD, ASC_QUOTE: PSEUDO_H_WITH_DOT, 0x7e: PSEUDO_i_WITH_DIAERESIS, ASC_X: PSEUDO_h_WITH_BREVE, ASC_NUMBER: PSEUDO_SMALL_ALEPH, ASC_o: PSEUDO_SMALL_AIN, 0x7c: PSEUDO_SMALL_YOD, ASC_H: PSEUDO_h_WITH_DOT, ASC_x: PSEUDO_h_WITH_LINE, 0xc8: PSEUDO_s, ASC_Q: PSEUDO_q, ASC_T: PSEUDO_t_WITH_LINE, ASC_D: PSEUDO_d_WITH_LINE, ASC_EXCLAMATION_MARK: PSEUDO_H, ASC_AT: PSEUDO_d_WITH_LINE, ASC_DOLLAR: PSEUDO_H_WITH_LINE, ASC_PERCENT: PSEUDO_H_WITH_BREVE, ASC_CIRCUMFLEX_ACCENT: ASC_LEFT_PARENTHESIS, ASC_AMPERSAND: PSEUDO_TOP_LEFT_HALF_BRACKET, ASC_LOW_LINE: PSEUDO_u_WITH_INVERTED_BREVE, ASC_PLUS: PSEUDO_i_WITH_INVERTED_BREVE, ASC_O: PSEUDO_H_WITH_DOT, ASC_V: PSEUDO_T_WITH_LINE, ASC_v: PSEUDO_T, ASC_EQUALS: PSEUDO_SUFFIX_PRONOMEN_SEPARATOR, ASC_e: PSEUDO_D, ASC_A: PSEUDO_RIGHT_HALF_RING, ASC_APOSTROPHE: PSEUDO_RIGHT_HALF_RING, 0x5c: PSEUDO_TOP_RIGHT_HALF_BRACKET, ASC_c: PSEUDO_S, 0xb3: PSEUDO_d, 0xb2: PSEUDO_t_WITH_LINE, ASC_E: PSEUDO_D_WITH_LINE, ASC_SECTION: PSEUDO_h_WITH_CURCUMFLEX, 0xdf: PSEUDO_t_WITH_CURCUMFLEX, 0xb5: PSEUDO_E, 0xc0: ASC_A, 0x2020: ASC_c, 0x2030: PSEUDO_T, 0x2122: PSEUDO_SMALL_ALEPH, 0xa1: ASC_LOW_LINE, 0xa3: PSEUDO_T_WITH_CURCUMFLEX, ASC_YEN: PSEUDO_e, 0xa9: PSEUDO_h_WITH_CURCUMFLEX, 0xc4: PSEUDO_Q, 0xc6: PSEUDO_d, 0xca: PSEUDO_CAPITAL_YOD, 0xcb: ASC_PLUS, 0xcf: PSEUDO_SMALL_YOD, 0xd2: ASC_O, 0xd3: ASC_o, 0xd6: PSEUDO_Q, 0xd9: PSEUDO_D_WITH_LINE, 0xdc: PSEUDO_S, 0xe6: PSEUDO_D, 0xe7: PSEUDO_t_WITH_LINE, 0xea: PSEUDO_e, 0xfb: PSEUDO_q, ASC_S: PSEUDO_s_WITH_CARON, ASC_C: PSEUDO_S_WITH_CARON, 0xbd: ASC_LEFT_PARENTHESIS},
               Format.UNICODE: {ASC_Y: PSEUDO_Y, ASC_L: PSEUDO_L, UN_I_WITH_DIAERESIS: PSEUDO_I_WITH_DIAERESIS, ASC_E: PSEUDO_E, ASC_e: PSEUDO_e, UN_SMALL_ALEPH: PSEUDO_SMALL_ALEPH, UN_CAPITAL_ALEPH: PSEUDO_CAPITAL_ALEPH, UN_SMALL_YOD: PSEUDO_SMALL_YOD, UN_CAPITAL_YOD: PSEUDO_CAPITAL_YOD, UN_i_WITH_INVERTED_BREVE: PSEUDO_i_WITH_INVERTED_BREVE, UN_I_WITH_INVERTED_BREVE: PSEUDO_I_WITH_INVERTED_BREVE, UN_RIGHT_HALF_RING: PSEUDO_RIGHT_HALF_RING, UN_SMALL_AIN: PSEUDO_SMALL_AIN, UN_CAPITAL_AIN: PSEUDO_CAPITAL_AIN, UN_u_WITH_INVERTED_BREVE: PSEUDO_u_WITH_INVERTED_BREVE, UN_U_WITH_INVERTED_BREVE: PSEUDO_U_WITH_INVERTED_BREVE, ASC_H: PSEUDO_H, UN_h_WITH_DOT: PSEUDO_h_WITH_DOT, UN_H_WITH_DOT: PSEUDO_H_WITH_DOT, UN_h_WITH_BREVE: PSEUDO_h_WITH_BREVE, UN_H_WITH_BREVE: PSEUDO_H_WITH_BREVE, UN_h_WITH_CURCUMFLEX: PSEUDO_h_WITH_CURCUMFLEX, UN_H_WITH_CURCUMFLEX: PSEUDO_H_WITH_CURCUMFLEX, UN_h_WITH_LINE: PSEUDO_h_WITH_LINE, UN_H_WITH_LINE: PSEUDO_H_WITH_LINE, ASC_S: PSEUDO_S, UN_s_WITH_CARON: PSEUDO_s_WITH_CARON, UN_S_WITH_CARON: PSEUDO_S_WITH_CARON, ASC_q: PSEUDO_q, ASC_Q: PSEUDO_Q, ASC_T: PSEUDO_T, UN_t_WITH_CURCUMFLEX: PSEUDO_t_WITH_CURCUMFLEX, UN_T_WITH_CURCUMFLEX: PSEUDO_T_WITH_CURCUMFLEX, UN_t_WITH_LINE: PSEUDO_t_WITH_LINE, UN_T_WITH_LINE: PSEUDO_T_WITH_LINE, ASC_D: PSEUDO_D, UN_d_WITH_LINE: PSEUDO_d_WITH_LINE, UN_D_WITH_LINE: PSEUDO_D_WITH_LINE, ASC_DOT: PSEUDO_DOT, UN_MIDDLE_DOT: PSEUDO_MIDDLE_DOT, ASC_COLON: PSEUDO_COLON, UN_SUFFIX_PRONOMEN_SEPARATOR: PSEUDO_SUFFIX_PRONOMEN_SEPARATOR, UN_TOP_LEFT_HALF_BRACKET: PSEUDO_TOP_LEFT_HALF_BRACKET, UN_TOP_RIGHT_HALF_BRACKET: PSEUDO_TOP_RIGHT_HALF_BRACKET, UN_LEFT_ANGLE_BRACKET: PSEUDO_LEFT_ANGLE_BRACKET, UN_RIGHT_ANGLE_BRACKET: PSEUDO_RIGHT_ANGLE_BRACKET, UN_TOP_LEFT_HALF_BRACKET: PSEUDO_TOP_LEFT_HALF_BRACKET, UN_TOP_RIGHT_HALF_BRACKET: PSEUDO_TOP_RIGHT_HALF_BRACKET, UN_LEFT_ANGLE_BRACKET: PSEUDO_LEFT_ANGLE_BRACKET, UN_RIGHT_ANGLE_BRACKET: PSEUDO_RIGHT_ANGLE_BRACKET, UN_MIDDLE_DOT: PSEUDO_MIDDLE_DOT, ASC_D: PSEUDO_D, ASC_H: PSEUDO_H, ASC_S: PSEUDO_S, ASC_T: PSEUDO_T, UN_SMALL_ALEPH: PSEUDO_SMALL_ALEPH, UN_CAPITAL_ALEPH: PSEUDO_SMALL_ALEPH, 0x21d: PSEUDO_SMALL_ALEPH, 0x21c: PSEUDO_SMALL_ALEPH, UN_CAPITAL_AIN: PSEUDO_SMALL_AIN, UN_SMALL_AIN: PSEUDO_SMALL_AIN, 0x2bf: PSEUDO_SMALL_AIN, 0xec41: PSEUDO_d_WITH_LINE, UN_H_WITH_LINE: PSEUDO_H_WITH_LINE, UN_H_WITH_CURCUMFLEX: PSEUDO_H_WITH_CURCUMFLEX, UN_h_WITH_CURCUMFLEX: PSEUDO_h_WITH_CURCUMFLEX, 0xec42: PSEUDO_SMALL_ALEPH, 0xec43: PSEUDO_SMALL_AIN, UN_i_WITH_INVERTED_BREVE: PSEUDO_i_WITH_INVERTED_BREVE, UN_u_WITH_INVERTED_BREVE: PSEUDO_u_WITH_INVERTED_BREVE, 0xec46: PSEUDO_SMALL_YOD, 0xec49: PSEUDO_CAPITAL_YOD, UN_SUFFIX_PRONOMEN_SEPARATOR: PSEUDO_SUFFIX_PRONOMEN_SEPARATOR, UN_k_WITH_DOT: PSEUDO_q, UN_K_WITH_DOT: PSEUDO_Q, UN_s_WITH_ACUTE: PSEUDO_s, UN_S_WITH_ACUTE: PSEUDO_S, UN_t_WITH_DOT: ASC_d, UN_T_WITH_DOT: ASC_D, UN_c_WITH_CARON: PSEUDO_t_WITH_LINE, UN_C_WITH_CARON: PSEUDO_T_WITH_LINE},
               Format.TRLIT_CG_TIMES: {ASC_Y: PSEUDO_Y, ASC_L: 0x2E25, UN_I_WITH_DIAERESIS: PSEUDO_I_WITH_DIAERESIS, ASC_E: PSEUDO_E, ASC_e: PSEUDO_e, ASC_x: PSEUDO_h_WITH_BREVE, ASC_A: PSEUDO_SMALL_ALEPH, ASC_a: PSEUDO_SMALL_AIN, ASC_i: PSEUDO_SMALL_YOD, ASC_H: PSEUDO_h_WITH_DOT, ASC_X: PSEUDO_h_WITH_LINE, ASC_c: PSEUDO_s, ASC_S: PSEUDO_s_WITH_CARON, ASC_q: PSEUDO_q, ASC_T: PSEUDO_t_WITH_LINE, ASC_D: PSEUDO_d_WITH_LINE, ASC_o: PSEUDO_q, 0x30: PSEUDO_H, 0x31: PSEUDO_H_WITH_DOT, 0x32: PSEUDO_H_WITH_BREVE, 0x33: PSEUDO_H_WITH_LINE, 0x34: PSEUDO_S, 0x35: PSEUDO_S_WITH_CARON, 0x36: PSEUDO_T, 0x37: PSEUDO_T_WITH_LINE, 0x38: PSEUDO_D, 0x39: PSEUDO_D_WITH_LINE, ASC_Q: PSEUDO_Q, ASC_I: PSEUDO_CAPITAL_YOD, ASC_O: PSEUDO_Q, ASC_C: PSEUDO_S, ASC_V: PSEUDO_T_WITH_CURCUMFLEX, ASC_v: PSEUDO_t_WITH_CURCUMFLEX, ASC_EQUALS: PSEUDO_SUFFIX_PRONOMEN_SEPARATOR},
               Format.TRLIT_CG_TIMES_2023: {ASC_L: 0x2E25, UN_I_WITH_DIAERESIS: PSEUDO_I_WITH_DIAERESIS, ASC_E: PSEUDO_E, ASC_e: PSEUDO_e, 0x7e: PSEUDO_TOP_LEFT_HALF_BRACKET, ASC_AT: PSEUDO_t_WITH_LINE, ASC_NUMBER: PSEUDO_TOP_RIGHT_HALF_BRACKET, ASC_DOLLAR: PSEUDO_d_WITH_LINE, ASC_ASTERISK: PSEUDO_RIGHT_HALF_RING, ASC_u: PSEUDO_h_WITH_CURCUMFLEX, ASC_Y: PSEUDO_i_WITH_DIAERESIS, ASC_x: PSEUDO_h_WITH_BREVE, ASC_A: PSEUDO_SMALL_ALEPH, ASC_a: PSEUDO_SMALL_AIN, ASC_i: PSEUDO_SMALL_YOD, ASC_H: PSEUDO_h_WITH_DOT, ASC_X: PSEUDO_h_WITH_LINE, ASC_c: PSEUDO_s, ASC_S: PSEUDO_s_WITH_CARON, ASC_q: PSEUDO_k, ASC_T: PSEUDO_t_WITH_LINE, ASC_D: PSEUDO_d_WITH_LINE, ASC_o: PSEUDO_q, 0x30: PSEUDO_H, 0x31: PSEUDO_H_WITH_DOT, 0x32: PSEUDO_H_WITH_BREVE, 0x33: PSEUDO_H_WITH_LINE, 0x34: PSEUDO_S, 0x35: PSEUDO_S_WITH_CARON, 0x36: PSEUDO_T, 0x37: PSEUDO_T_WITH_LINE, 0x38: PSEUDO_D, 0x39: PSEUDO_D_WITH_LINE, ASC_Q: PSEUDO_K, ASC_I: PSEUDO_CAPITAL_YOD, ASC_O: PSEUDO_Q, ASC_C: PSEUDO_S, ASC_V: PSEUDO_T_WITH_CURCUMFLEX, ASC_v: PSEUDO_t_WITH_CURCUMFLEX, ASC_AMPERSAND: ASC_AMPERSAND, ASC_EXCLAMATION_MARK: PSEUDO_d, ASC_EQUALS: PSEUDO_SUFFIX_PRONOMEN_SEPARATOR, ASC_CIRCUMFLEX_ACCENT: PSEUDO_H_WITH_CURCUMFLEX, 0x3c: PSEUDO_LEFT_ANGLE_BRACKET, 0x3e: PSEUDO_RIGHT_ANGLE_BRACKET},
               Format.TRANSLITERATION: {ASC_Y: PSEUDO_Y, ASC_L: PSEUDO_L, UN_I_WITH_DIAERESIS: PSEUDO_I_WITH_DIAERESIS, ASC_E: PSEUDO_E, ASC_e: PSEUDO_e, ASC_x: PSEUDO_h_WITH_BREVE, ASC_A: PSEUDO_SMALL_ALEPH, ASC_a: PSEUDO_SMALL_AIN, ASC_i: PSEUDO_SMALL_YOD, ASC_H: PSEUDO_h_WITH_DOT, ASC_X: PSEUDO_h_WITH_LINE, ASC_c: PSEUDO_s, ASC_S: PSEUDO_s_WITH_CARON, ASC_q: PSEUDO_q, ASC_T: PSEUDO_t_WITH_LINE, ASC_D: PSEUDO_d_WITH_LINE, ASC_o: PSEUDO_q, ASC_EXCLAMATION_MARK: PSEUDO_H, ASC_AT: PSEUDO_H_WITH_DOT, ASC_NUMBER: PSEUDO_H_WITH_BREVE, ASC_DOLLAR: PSEUDO_H_WITH_LINE, ASC_PERCENT: PSEUDO_S, ASC_CIRCUMFLEX_ACCENT: PSEUDO_S_WITH_CARON, ASC_YEN: PSEUDO_S_WITH_CARON, ASC_AMPERSAND: PSEUDO_T, ASC_ASTERISK: PSEUDO_T_WITH_LINE, ASC_SECTION: PSEUDO_T_WITH_LINE, ASC_LOW_LINE: PSEUDO_D, ASC_PLUS: PSEUDO_D_WITH_LINE, ASC_Q: PSEUDO_Q, ASC_I: PSEUDO_CAPITAL_YOD, ASC_O: PSEUDO_Q, ASC_C: PSEUDO_S, ASC_V: PSEUDO_h_WITH_CURCUMFLEX, ASC_v: PSEUDO_t_WITH_CURCUMFLEX, ASC_EQUALS: PSEUDO_SUFFIX_PRONOMEN_SEPARATOR},
               Format.COMMON_D: {0x1EC8: PSEUDO_CAPITAL_YOD, 0x1EC9: PSEUDO_SMALL_YOD, UN_i_WITH_DIAERESIS: PSEUDO_i_WITH_DIAERESIS, ASC_DOT: PSEUDO_DOT, ASC_COLON: PSEUDO_COLON, ASC_SUFFIX_PRONOMEN_SEPARATOR: PSEUDO_SUFFIX_PRONOMEN_SEPARATOR, ASC_b: PSEUDO_b, ASC_d: PSEUDO_d, ASC_f: PSEUDO_f, ASC_g: PSEUDO_g, ASC_h: PSEUDO_h, ASC_j: PSEUDO_SMALL_YOD, ASC_k: PSEUDO_k, ASC_l: PSEUDO_l, ASC_m: PSEUDO_m, ASC_n: PSEUDO_n, ASC_p: PSEUDO_p, ASC_q: PSEUDO_q, ASC_r: PSEUDO_r, ASC_s: PSEUDO_s, ASC_t: PSEUDO_t, ASC_w: PSEUDO_w, ASC_y: PSEUDO_y, ASC_z: PSEUDO_z, ASC_B: PSEUDO_B, ASC_F: PSEUDO_F, ASC_G: PSEUDO_G, ASC_J: PSEUDO_CAPITAL_YOD, ASC_K: PSEUDO_K, ASC_M: PSEUDO_M, ASC_N: PSEUDO_N, ASC_P: PSEUDO_P, ASC_Q: PSEUDO_Q, ASC_R: PSEUDO_R, ASC_W: PSEUDO_W, ASC_Z: PSEUDO_Z}}
for imp_dict in IMPORT_DICT:
    IMPORT_DICT[imp_dict].update(IMPORT_DICT[Format.COMMON_D])
IMPORT_DICT_S_FOR_Z = {Format.UMSCHRIFT_TTN: {ASC_s: PSEUDO_z, ASC_c: PSEUDO_Z},
                       Format.UNICODE: {ASC_s: PSEUDO_z, ASC_S: PSEUDO_Z},
                       Format.TRLIT_CG_TIMES: {ASC_s: PSEUDO_z, 0x34: PSEUDO_Z},
                       Format.TRLIT_CG_TIMES_2023: {ASC_s: PSEUDO_z, 0x34: PSEUDO_Z},
                       Format.TRANSLITERATION: {ASC_s: PSEUDO_z, ASC_PERCENT: PSEUDO_Z}}
EXPORT_DICT = {Format.UNICODE: {PSEUDO_SMALL_ALEPH: UN_SMALL_ALEPH, PSEUDO_CAPITAL_ALEPH: UN_CAPITAL_ALEPH, PSEUDO_SMALL_YOD: UN_SMALL_YOD, PSEUDO_CAPITAL_YOD: UN_CAPITAL_YOD, PSEUDO_e: ASC_e, PSEUDO_E: ASC_E, PSEUDO_y: ASC_y, PSEUDO_Y: ASC_Y, PSEUDO_i_WITH_DIAERESIS: UN_i_WITH_DIAERESIS, PSEUDO_I_WITH_DIAERESIS: UN_I_WITH_DIAERESIS, PSEUDO_i_WITH_INVERTED_BREVE: UN_i_WITH_INVERTED_BREVE, PSEUDO_I_WITH_INVERTED_BREVE: UN_I_WITH_INVERTED_BREVE, PSEUDO_RIGHT_HALF_RING: UN_RIGHT_HALF_RING, PSEUDO_SMALL_AIN: UN_SMALL_AIN, PSEUDO_CAPITAL_AIN: UN_CAPITAL_AIN, PSEUDO_w: ASC_w, PSEUDO_W: ASC_W, PSEUDO_u_WITH_INVERTED_BREVE: UN_u_WITH_INVERTED_BREVE, PSEUDO_U_WITH_INVERTED_BREVE: UN_U_WITH_INVERTED_BREVE, PSEUDO_b: ASC_b, PSEUDO_B: ASC_B, PSEUDO_p: ASC_p, PSEUDO_P: ASC_P, PSEUDO_f: ASC_f, PSEUDO_F: ASC_F, PSEUDO_m: ASC_m, PSEUDO_M: ASC_M, PSEUDO_n: ASC_n, PSEUDO_N: ASC_N, PSEUDO_r: ASC_r, PSEUDO_R: ASC_R, PSEUDO_l: ASC_l, PSEUDO_L: ASC_L, PSEUDO_h: ASC_h, PSEUDO_H: ASC_H, PSEUDO_h_WITH_DOT: UN_h_WITH_DOT, PSEUDO_H_WITH_DOT: UN_H_WITH_DOT, PSEUDO_h_WITH_BREVE: UN_h_WITH_BREVE, PSEUDO_H_WITH_BREVE: UN_H_WITH_BREVE,
                                PSEUDO_h_WITH_CURCUMFLEX: UN_h_WITH_CURCUMFLEX, PSEUDO_H_WITH_CURCUMFLEX: UN_H_WITH_CURCUMFLEX, PSEUDO_h_WITH_LINE: UN_h_WITH_LINE, PSEUDO_H_WITH_LINE: UN_H_WITH_LINE, PSEUDO_z: ASC_z, PSEUDO_Z: ASC_Z, PSEUDO_s: ASC_s, PSEUDO_S: ASC_S, PSEUDO_s_WITH_CARON: UN_s_WITH_CARON, PSEUDO_S_WITH_CARON: UN_S_WITH_CARON, PSEUDO_q: ASC_q, PSEUDO_Q: ASC_Q, PSEUDO_k: ASC_k, PSEUDO_K: ASC_K, PSEUDO_g: ASC_g, PSEUDO_G: ASC_G, PSEUDO_t: ASC_t, PSEUDO_T: ASC_T, PSEUDO_t_WITH_CURCUMFLEX: UN_t_WITH_CURCUMFLEX, PSEUDO_T_WITH_CURCUMFLEX: UN_T_WITH_CURCUMFLEX, PSEUDO_t_WITH_LINE: UN_t_WITH_LINE, PSEUDO_T_WITH_LINE: UN_T_WITH_LINE, PSEUDO_d: ASC_d, PSEUDO_D: ASC_D, PSEUDO_d_WITH_LINE: UN_d_WITH_LINE, PSEUDO_D_WITH_LINE: UN_D_WITH_LINE, PSEUDO_SUFFIX_PRONOMEN_SEPARATOR: UN_SUFFIX_PRONOMEN_SEPARATOR, PSEUDO_DOT: ASC_DOT, PSEUDO_COLON: ASC_COLON, PSEUDO_MIDDLE_DOT: UN_MIDDLE_DOT, PSEUDO_TOP_LEFT_HALF_BRACKET: UN_TOP_LEFT_HALF_BRACKET, PSEUDO_TOP_RIGHT_HALF_BRACKET: UN_TOP_RIGHT_HALF_BRACKET, PSEUDO_LEFT_ANGLE_BRACKET: UN_LEFT_ANGLE_BRACKET, PSEUDO_RIGHT_ANGLE_BRACKET: UN_RIGHT_ANGLE_BRACKET},
               Format.TRANSLITERATION: {ASC_GRAVIS: ASC_GRAVIS, ASC_HYPHEN_MINUS: ASC_HYPHEN_MINUS, ASC_EQUALS: ASC_EQUALS, ASC_TILDE: ASC_TILDE,
                                        PSEUDO_H: ASC_EXCLAMATION_MARK, PSEUDO_H_WITH_DOT: ASC_AT, PSEUDO_H_WITH_BREVE: ASC_NUMBER, PSEUDO_H_WITH_LINE: ASC_DOLLAR,
                                        PSEUDO_S: ASC_PERCENT, PSEUDO_S_WITH_CARON: ASC_CIRCUMFLEX_ACCENT, PSEUDO_T: ASC_AMPERSAND, PSEUDO_T_WITH_LINE: ASC_ASTERISK,
                                        ASC_LEFT_PARENTHESIS: ASC_LEFT_PARENTHESIS, ASC_RIGHT_PARENTHESIS: ASC_RIGHT_PARENTHESIS, PSEUDO_D: ASC_LOW_LINE, PSEUDO_D_WITH_LINE: ASC_PLUS,
                                        PSEUDO_w: ASC_w, PSEUDO_e: ASC_e, PSEUDO_r: ASC_r, PSEUDO_t: ASC_t, PSEUDO_y: ASC_y, ASC_u: ASC_u,
                                        PSEUDO_SMALL_YOD: ASC_i, PSEUDO_q: ASC_o, PSEUDO_p: ASC_p,
                                        ASC_LEFT_SQUARE_BRACKET: ASC_LEFT_SQUARE_BRACKET, ASC_RIGHT_SQUARE_BRACKET: ASC_RIGHT_SQUARE_BRACKET,
                                        PSEUDO_W: ASC_W, PSEUDO_E: ASC_E, PSEUDO_R: ASC_R, PSEUDO_Y: ASC_Y, ASC_U: ASC_U,
                                        PSEUDO_CAPITAL_YOD: ASC_I, PSEUDO_Q: ASC_O, PSEUDO_P: ASC_P,
                                        ASC_LEFT_CURLY_BRACKET: ASC_LEFT_CURLY_BRACKET, ASC_RIGHT_CURLY_BRACKET: ASC_RIGHT_CURLY_BRACKET,
                                        PSEUDO_s: ASC_s, PSEUDO_d: ASC_d, PSEUDO_f: ASC_f, PSEUDO_g: ASC_g, PSEUDO_F: ASC_F, PSEUDO_G: ASC_G, PSEUDO_h: ASC_h,
                                        PSEUDO_k: ASC_k, PSEUDO_l: ASC_l, PSEUDO_K: ASC_K, PSEUDO_L: ASC_L,
                                        PSEUDO_s_WITH_CARON: ASC_S, PSEUDO_d_WITH_LINE: ASC_D, PSEUDO_h_WITH_DOT: ASC_H,
                                        PSEUDO_z: ASC_z, PSEUDO_Z: ASC_Z, PSEUDO_h_WITH_BREVE: ASC_x, PSEUDO_t_WITH_CURCUMFLEX: ASC_v, PSEUDO_T_WITH_CURCUMFLEX: ASC_v,
                                        PSEUDO_b: ASC_b, PSEUDO_n: ASC_n, PSEUDO_m: ASC_m, PSEUDO_B: ASC_B, PSEUDO_N: ASC_N, PSEUDO_M: ASC_M,
                                        PSEUDO_h_WITH_LINE: ASC_X, PSEUDO_h_WITH_CURCUMFLEX: ASC_V, PSEUDO_H_WITH_CURCUMFLEX: ASC_V,
                                        ASC_QUESTION_MARK: ASC_QUESTION_MARK, ASC_COMMA: ASC_COMMA,
                                        ASC_SEMICOLON: ASC_SEMICOLON, ASC_APOSTROPHE: ASC_APOSTROPHE, ASC_SPACE: ASC_SPACE,
                                        ASC_SOLIDUS: ASC_SOLIDUS, ASC_LESS_THAN_SIGN: ASC_LESS_THAN_SIGN,  ASC_GREATER_THAN_SIGN: ASC_GREATER_THAN_SIGN,
                                        ASC_VERTICAL_LINE: ASC_VERTICAL_LINE, UN_NO_BREAK_SPACE: UN_NO_BREAK_SPACE,
                                        UN_DIVISION_SIGN: UN_DIVISION_SIGN, UN_LATIN_SMALL_LETTER_O_WITH_STROKE: UN_LATIN_SMALL_LETTER_O_WITH_STROKE, UN_LATIN_SMALL_LETTER_THORN: UN_LATIN_SMALL_LETTER_THORN,
                                        PSEUDO_DOT: ASC_DOT, PSEUDO_COLON: ASC_COLON, PSEUDO_SUFFIX_PRONOMEN_SEPARATOR: ASC_EQUALS, PSEUDO_LEFT_ANGLE_BRACKET: ASC_LESS_THAN_SIGN,
                                        PSEUDO_RIGHT_ANGLE_BRACKET: ASC_GREATER_THAN_SIGN,
                                        PSEUDO_SMALL_ALEPH: ASC_A, PSEUDO_CAPITAL_ALEPH: ASC_A, PSEUDO_SMALL_AIN: ASC_a, PSEUDO_CAPITAL_AIN: ASC_A,
                                        PSEUDO_i_WITH_DIAERESIS: ASC_y, PSEUDO_I_WITH_DIAERESIS: ASC_Y}}
for a in range(ASC_ZERO, ASC_NINE):
    EXPORT_DICT[Format.TRANSLITERATION][a] = a
for a in range(UN_FEMININE_ORDINAL_INDICATOR, UN_PILCROW_SIGN):
    EXPORT_DICT[Format.TRANSLITERATION][a] = a
for a in range(UN_CEDILLA, UN_INVERTED_QUESTION_MARK):
    EXPORT_DICT[Format.TRANSLITERATION][a] = a
for a in range(UN_MULTIPLICATION_SIGN, UN_LATIN_SMALL_LETTER_SHARP_S):
    EXPORT_DICT[Format.TRANSLITERATION][a] = a
for a in range(UN_EN_QUAD, UN_NOMINAL_DIGIT_SHAPES):
    EXPORT_DICT[Format.TRANSLITERATION][a] = a
EXPORT_DICT_K_WITH_DOT = {Format.UNICODE: {
    PSEUDO_Q: UN_K_WITH_DOT, PSEUDO_q: UN_k_WITH_DOT},
    Format.TRANSLITERATION:   {PSEUDO_Q: ASC_Q, PSEUDO_q: ASC_q}}
EXPORT_DICT_J_FOR_YOD = {Format.UNICODE: {
    PSEUDO_CAPITAL_YOD: ASC_J, PSEUDO_SMALL_YOD: ASC_j},
    Format.TRANSLITERATION: {
    PSEUDO_CAPITAL_YOD: ASC_J, PSEUDO_SMALL_YOD: ASC_j}}
EXPORT_DICT_S_ACUTE = {Format.UNICODE: {PSEUDO_z: ASC_s, PSEUDO_Z: ASC_S, PSEUDO_s: UN_s_WITH_ACUTE, PSEUDO_S: UN_S_WITH_ACUTE},
                       Format.TRANSLITERATION:   {PSEUDO_z: ASC_s, PSEUDO_Z: ASC_PERCENT, PSEUDO_s: ASC_c, PSEUDO_S: ASC_C}}

EXPORT_MULTICHAR_DICT = {Format.UNICODE: {PSEUDO_i_WITH_INVERTED_BREVE: array.array('L', [(ASC_i), (UN_COMBINING_INVERTED_BREVE)]), PSEUDO_I_WITH_INVERTED_BREVE: array.array('L', [(ASC_I), (UN_COMBINING_INVERTED_BREVE)]), PSEUDO_u_WITH_INVERTED_BREVE: array.array('L', [(ASC_u), (UN_COMBINING_INVERTED_BREVE)]), PSEUDO_U_WITH_INVERTED_BREVE: array.array(
    'L', [(ASC_U), (UN_COMBINING_INVERTED_BREVE)]), PSEUDO_H_WITH_LINE: array.array('L', [(ASC_H), (UN_COMBINING_MACRON_BELOW)]), PSEUDO_h_WITH_CURCUMFLEX: array.array('L', [(ASC_h), (UN_COMBINING_CIRCUMFLEX_BELOW)]), PSEUDO_H_WITH_CURCUMFLEX: array.array('L', [(ASC_H), (UN_COMBINING_CIRCUMFLEX_BELOW)])},
    Format.TRANSLITERATION: {}}


class UmschString(array.array):
    def __getitem__(self, key):  # makes sure that slicing does not result in object type change
        if type(key) == slice:
            return UmschString(super().__getitem__(key))
        return super().__getitem__(key)

    def __new__(cls, initializer=[], source_format: Format = Format.UNICODE, flags=0):
        if type(initializer) == str:
            return UmschString._string_to_UmschrString(initializer, source_format, flags)
        # Uses unsigned long ints to store 4-byte chars
        return (super().__new__(cls, 'L', initializer))

# Imports data from a string to an Umschrift array
    def _string_to_UmschrString(value: str, source_format: Format = Format.UNICODE, flags=0):
        i = 1
        res = UmschString()
        next_char = ord(value[0])
        yod_flag = [0]
        import_dict = IMPORT_DICT[source_format].copy()
        if flags & UmImport.S_FOR_Z:
            import_dict.update(IMPORT_DICT_S_FOR_Z[source_format])

        while i <= len(value):
            current_char = next_char
            next_char = ord(value[i]) if i < (len(value)) else 0
            converted_char = UmschString._import_char(
                import_dict, current_char, next_char, source_format, yod_flag)
            if (converted_char):
                res.append(converted_char)
            i += 1
        return res

    def _import_char(import_dict, current_char, next_char, source_format, yod_flag):
        ignored_chars = [UN_COMBINING_MACRON_BELOW, UN_COMBINING_CIRCUMFLEX_BELOW, UN_COMBINING_INVERTED_BREVE,
                         UN_COMBINING_RIGHT_HALF_RING_ABOVE, UN_COMBINING_CYRILLIC_PSILI_PNEUMATA, UN_COMBINING_DOT_BELOW]
        if current_char in ignored_chars:
            return 0
        if next_char == UN_COMBINING_MACRON_BELOW:
            return UN_DECODE_BEFORE_COMBINING_MACRON[current_char]
        if next_char == UN_COMBINING_CIRCUMFLEX_BELOW:
            return UN_DECODE_BEFORE_COMBINING_CIRCUMFLEX[current_char]
        if next_char == UN_COMBINING_INVERTED_BREVE:
            return UN_DECODE_BEFORE_COMBINING_INVERTED_BREVE[current_char]
        if next_char in [UN_COMBINING_RIGHT_HALF_RING_ABOVE, UN_COMBINING_CYRILLIC_PSILI_PNEUMATA]:
            return UN_DECODE_BEFORE_COMBINING_HALF_RING_ABOVE[current_char]
        if next_char == UN_COMBINING_DOT_BELOW:
            return UN_DECODE_BEFORE_COMBINING_DOT_BELOW[current_char]
        if (next_char in [ASC_j, ASC_J]) and (current_char in [ASC_j, ASC_J]):
            if yod_flag[0] == 0:
                yod_flag[0] = current_char
                return 0
            else:
                prev = yod_flag[0]
                yod_flag[0] = current_char
                current_char = prev
        elif yod_flag[0]:
            current_char = {ASC_j: ASC_y, ASC_J: ASC_Y}[yod_flag[0]]
            yod_flag[0] = 0
        if current_char in import_dict:
            return import_dict[current_char]
        return current_char

    def to_pseudo(self):  # exports array as a string of pseudo characters that can be used for sorting and comparison using binary-based locales (for example in databases)
        if byteorder == "little":
            return self.tobytes().decode("utf_32_le")
        return self.tobytes().decode("utf_32_be")

    def to_unicode(self, flags=0):  # exports array content as a Unicode-formatted string

        return self._export_string(Format.UNICODE, flags)

    def to_transliteration(self, flags=0):
        return self._export_string(Format.TRANSLITERATION, flags, True)

    def upper(self):
        res = UmschString()
        for char in self:
            if (cased(char)):
                res.append(char - (char & 1))
            else:
                res.append(char)
        return res

    def lower(self):
        res = UmschString()
        for char in self:
            if (cased(char)):
                res.append(char + (~char & 1))
            else:
                res.append(char)
        return res

    def index(self, sub: array.array, start=None, end=None):
        res = self.find(sub, start, end)
        if res == -1:
            raise ValueError("Not found")
        else:
            return res

    def find_all(self, sub: array.array, start=None, end=None):
        NOT_FOUND = -1
        slice_start, _, _ = slice(start, end).indices(len(self))
        pos = slice_start
        res = []
        while pos > NOT_FOUND:
            pos = self.find(sub, pos, end)
            if pos > NOT_FOUND:
                res.append(pos)
                pos += 1
        return res

    def find(self, sub: array.array, start=None, end=None):
        slice_start, slice_end, _ = slice(start, end).indices(len(self))
        pos = slice_start
        sub_length = len(sub)
        while pos <= slice_end-sub_length:
            if self[pos:pos+sub_length] == sub:
                return pos
            pos += 1
        return -1

    def replace(self, old: array.array, new: array.array, count=None):
        pos = 0
        replaces = self.find_all(old)[None:count]
        old_len = len(old)
        res = UmschString()
        for rep in replaces:
            res.extend(self[pos:rep])
            res.extend(new)
            pos = rep + old_len
        res.extend(self[pos:None])
        return res

    def filter(self, flags=0):
        between_parentheses = False
        filtered_signs = []
        replaces = {}
        res = UmschString()
        if flags & UmFilter.MORPH:
            filtered_signs.extend(
                [PSEUDO_DOT, PSEUDO_COLON, PSEUDO_MIDDLE_DOT])
        if flags & UmFilter.SUFF_PRON:
            filtered_signs.extend([PSEUDO_SUFFIX_PRONOMEN_SEPARATOR])
        if flags & UmFilter.BRACKETS:
            filtered_signs.extend([PSEUDO_TOP_LEFT_HALF_BRACKET, PSEUDO_TOP_RIGHT_HALF_BRACKET, PSEUDO_LEFT_ANGLE_BRACKET, PSEUDO_RIGHT_ANGLE_BRACKET, ASC_LEFT_PARENTHESIS, ASC_RIGHT_PARENTHESIS,
                                  ASC_LEFT_SQUARE_BRACKET, ASC_RIGHT_SQUARE_BRACKET, ASC_LESS_THAN_SIGN, ASC_GREATER_THAN_SIGN, ASC_LEFT_CURLY_BRACKET, ASC_RIGHT_CURLY_BRACKET, ASC_VERTICAL_LINE])
        if flags & UmFilter.PUNCT:
            filtered_signs.extend(
                [PSEUDO_DOT, ASC_COMMA, ASC_QUESTION_MARK, ASC_EXCLAMATION_MARK, ASC_QUOTE])
        if flags & UmFilter.DIGITS:
            filtered_signs.extend(range(ASC_ZERO, ASC_NINE))
        if flags & UmFilter.HYPHENS:
            replaces.update({ASC_HYPHEN_MINUS: ASC_SPACE,
                            UN_MINUS_SIGN: ASC_SPACE})
            replaces.update(dict.fromkeys(
                range(UN_HYPHEN, UN_HORIZONTAL_BAR), ASC_SPACE))
        if flags & UmFilter.REPLACE_I_WITH_DIAERESIS:
            replaces.update({PSEUDO_i_WITH_DIAERESIS: PSEUDO_y,
                             PSEUDO_I_WITH_DIAERESIS: PSEUDO_Y})
        if flags & UmFilter.REPLACE_INVERTED_BREVES:
            replaces.update({PSEUDO_i_WITH_INVERTED_BREVE: PSEUDO_SMALL_YOD,
                             PSEUDO_I_WITH_INVERTED_BREVE: PSEUDO_CAPITAL_YOD,
                            PSEUDO_u_WITH_INVERTED_BREVE: PSEUDO_w,
                            PSEUDO_U_WITH_INVERTED_BREVE: PSEUDO_W})
        if flags & UmFilter.REPLACE_UNCERTAIN_CONSONANT:
            replaces.update({PSEUDO_RIGHT_HALF_RING: PSEUDO_SMALL_ALEPH})
        if flags & UmFilter.REPLACE_Z:
            replaces.update({PSEUDO_Z: PSEUDO_S, PSEUDO_z: PSEUDO_s})

        i = 0
        while i < len(self):
            char = self[i]
            if (flags & UmFilter.FACULTATIVE) and between_parentheses:
                between_parentheses = not (char == ASC_RIGHT_PARENTHESIS)
            elif (flags & UmFilter.FACULTATIVE) and char == ASC_LEFT_PARENTHESIS:
                between_parentheses = True
            elif replaces and char in replaces:
                res.append(replaces[char])
            elif not char in filtered_signs:
                res.append(char)
            i += 1
        if flags & UmFilter.LOWER:
            return res.lower()
        return res

    def endswith(self, sub: array.array, start=None, end=None):
        slice_obj = slice(start, end)
        sliced = self[slice_obj]
        if len(sub) <= len(sliced) and sliced[-1*len(sub):None] == sub:
            return True
        return False

    def startswith(self, sub: array.array, start=None, end=None):
        slice_obj = slice(start, end)
        sliced = self[slice_obj]
        if len(sub) <= len(sliced) and sliced[None:len(sub)] == sub:
            return True
        return False
    # Exports data from an Umschrift array into a string

    def _export_string(self, output_format: Format, flags=0, discard_not_found: bool = False):
        input = UmschString(self)

        if flags & UmExport.REPLACE_I_WITH_DIAERESIS:

            input = input.replace(UmschString([PSEUDO_I_WITH_DIAERESIS]), UmschString([PSEUDO_Y])).replace(
                UmschString([PSEUDO_i_WITH_DIAERESIS]), UmschString([PSEUDO_y]))

        if flags & UmExport.JJ_FOR_DOUBLE_YOD:
            input = input.replace(UmschString([PSEUDO_y]), UmschString([ASC_j, ASC_j])).replace(UmschString([PSEUDO_Y]), UmschString([ASC_J, ASC_j])).replace(
                UmschString([PSEUDO_I_WITH_DIAERESIS]), UmschString([ASC_J, ASC_j])).replace(UmschString([PSEUDO_i_WITH_DIAERESIS]), UmschString([ASC_j, ASC_j]))

        if (not input):
            return str()
        res = array.array('L')
        export_dict = EXPORT_DICT[output_format].copy()
        if flags & UmExport.K_WITH_DOT:
            export_dict.update(EXPORT_DICT_K_WITH_DOT[output_format])
        if flags & UmExport.J_FOR_YOD:
            export_dict.update(EXPORT_DICT_J_FOR_YOD[output_format])
        if flags & UmExport.Z_FOR_S_AND_S_FOR_S_ACUTE:
            export_dict.update(EXPORT_DICT_S_ACUTE[output_format])
        export_multichar_dict = EXPORT_MULTICHAR_DICT[output_format].copy()
        for char in input:
            if (char in export_multichar_dict):
                res.extend(export_multichar_dict[char])
            elif (char in export_dict):
                res.append((export_dict[char]))
            elif (not discard_not_found):
                res.append((char))
        if byteorder == "little":
            return res.tobytes().decode("utf_32_le")
        return res.tobytes().decode("utf_32_be")


def cased(char: int):
    if char >= PSEUDO_CAPITAL_ALEPH and char <= PSEUDO_d_WITH_LINE and char != PSEUDO_RIGHT_HALF_RING:
        return True
    else:
        return False


def from_pseudo(input: str):
    return UmschString([ord(s) for s in input])


def from_unicode(input: str, flags=0):
    return UmschString(input, Format.UNICODE, flags)


def from_umschrift_ttn(input: str, flags=0):
    return UmschString(input, Format.UMSCHRIFT_TTN, flags)


def from_trlit_cg_times(input: str, flags=0):
    return UmschString(input, Format.TRLIT_CG_TIMES, flags)


def from_trlit_cg_times_2023(input: str, flags=0):
    return UmschString(input, Format.TRLIT_CG_TIMES_2023, flags)


def from_transliteration(input: str, flags=0):
    return UmschString(input, Format.TRANSLITERATION, flags)
