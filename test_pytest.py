from umschriftpy import *
import sqlite3


def test_sort():
    """Loads transliteration strings to umschrift objects and sorts them using the biult-in sorted function."""
    # inputting several names as a list
    name_list = [from_transliteration("nfr-Htp"), from_transliteration(
        "aA-ptH"), from_transliteration("DHw.tj-nfr"), from_transliteration("Aw-jb")]
    # filtering list values
    name_list_filtered = [item.filter(UmFilter.CLEAN | UmFilter.LOWER)
                          for item in name_list]
    # using a standard Python function to sort items
    name_list_sorted = sorted(name_list_filtered)
    # outputting the sorted list as Unicode
    assert ([item.to_unicode() for item in name_list_sorted]) == [
        'ꜣw-ꞽb', 'ꜥꜣ-ptḥ', 'nfr-ḥtp', 'ḏḥwtꞽ-nfr']
    # >>> ['ꜣw-ꞽb', 'ꜥꜣ-ptḥ', 'nfr-ḥtp', 'ḏḥwtꞽ-nfr']


def test_pseudo():
    """Converts transliteration strings to pseudo codes, loads them in a sqlite database, sorts them in sqlite and outputs the strings back to umschrift objects."""
    name_list = [from_transliteration("nfr-Htp"), from_transliteration(
        "aA-ptH"), from_transliteration("DHw.tj-nfr"), from_transliteration("Aw-jb")]
    # filtering list values
    name_list_filtered = [item.filter(UmFilter.CLEAN | UmFilter.LOWER)
                          for item in name_list]

    pseudo_strings = [item.to_pseudo() for item in name_list_filtered]
    sconn = sqlite3.connect(":memory:")
    sconn.text_factory = str
    scur = sconn.cursor()
    scur.execute("""CREATE TABLE IF NOT EXISTS test(umschrift TEXT)""")
    for y in pseudo_strings:
        scur.execute("INSERT INTO test VALUES(?)", (y,))
    sconn.commit()
    scur.execute("SELECT umschrift FROM test ORDER BY umschrift")

    res_tup = scur.fetchall()
    result = [r[0] for r in res_tup]

    name_list_from_sqlite = [from_pseudo(r) for r in result]
    assert [i.to_unicode() for i in name_list_from_sqlite] == [
        'ꜣw-ꞽb', 'ꜥꜣ-ptḥ', 'nfr-ḥtp', 'ḏḥwtꞽ-nfr']


def test_filter():
    a = from_umschrift_ttn("O#.tj-o-jj#")  # imports an Umschrift_TTn string
    print(a.to_unicode())
    # >>> Ḥꜣ.tꞽ-ꜥ-yꜣ
    b = from_unicode("ḥꜣtꞽ ꜥ yꜣ")  # imports an Unicode string
    print(b.to_unicode())
    # >>> ḥꜣtꞽ ꜥ yꜣ
    # the strings are different because of different punctuation, lowercase and uppercase letters
    print(a == b)
    # >>> False
    a_filtered = a.filter(UmFilter.CLEAN | UmFilter.HYPHENS | UmFilter.LOWER)
    b_filtered = b.filter(UmFilter.CLEAN | UmFilter.HYPHENS |
                          UmFilter.LOWER)  # filters strings

    assert a_filtered == b_filtered


def test_find_umschriftttn():
    """Tests Umschrift_TTn imports."""
    a = r"+=@ACDEHOQSTX\_ceovx|~‰¦§©²³μÈËßçôŠ™£¥ÆÇÊÏÖÙÜæû!$%'"+'"'
    b = r"ḏdḏdi̯⸗ḏʾŠḏḎḥḤḲšṯḫ⸣u̯SDꜥTẖꞽïTꞽh̭h̭ṯdEs+ṱṯd~ꜣꜣṰedṮꞼꞽQḎSDqHH̱ḪʾḤ"

    au = from_umschrift_ttn(a)
    bu = from_unicode(b)

    assert au == bu[4:] and bu.find(au) == 4


def test_common_chars():
    a = from_unicode(r"gGtTp")
    b = UmschString([0xF139, 0xF138, 0xF13B, 0xF13A, 0xF119])
    assert a == b


def test_find_all():
    a = r"bdtpbdtptptptp"
    b = r"p"
    au = from_unicode(a)
    bu = from_unicode(b)
    assert au.find_all(bu, -5, -2) == [9, 11]
    assert au.find_all(bu, 4, 11) == [7, 9]
    assert au.find_all(bu, 4, -2) == [7, 9, 11]


def test_transliteration():
    """Tests Transliteration imports."""
    a = r"~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:||ZXCVBNM<>?qwertyuiop[]asdfghjkl;'\\zxcvbnm,./"
    b = r"~HḤḪH̱SŠTṮ()DḎḲWERṯYUꞼQP{}ꜣšḏFGḥJKL:||ZẖŚh̭BNM<>?ḳwertyuꞽqp[]ꜥsdfghjkl;'\\zḫśṱbnm,./"

    au = from_transliteration(a)
    bu = from_unicode(b)
    print(au)
    print(bu)
    assert au == bu


def test_trlitcgtimes():
    """Tests trlit_cg_times imports."""
    a = r"~@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:||ZXCVBNM<>?qwertyuiop[]asdfghjkl;'\\zxcvbnm,./"
    b = r"~@#$%^&*()_+ḲWERṯYUꞼQP{}ꜣšḏFGḥJK⸥:||ZẖŚṰBNM<>?ḳwertyuꞽqp[]ꜥsdfghjkl;'\\zḫśṱbnm,./"

    au = from_trlit_cg_times(a)
    bu = from_unicode(b)
    print(au)
    print(bu)
    assert au == bu


def test_trlitcgtimes2023():
    """Tests trlit_cg_times 2023 imports."""
    a = r"~@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:||ZXCVBNM<>?qwertyuiop[]asdfghjkl;'\\zxcvbnm,./"
    b = r"⸢č⸣č̣%H̭&ʾ()_+ḲWERṯïUꞼQP{}ꜣšḏFGḥJK⸥:||ZẖŚṰBNM⟨⟩?ḳwertyh̭ꞽqp[]ꜥsdfghjkl;'\\zḫśṱbnm,./"

    au = from_trlit_cg_times_2023(a)
    bu = from_unicode(b)
    print(au)
    print(bu)
    assert au == bu


def test_unicode():
    """Tests IFAO Unicode imports."""
    a = r"ʿȝḫẖỉḥḤḪšŠṯṮḏḎʿȝḫỈH̱nm"
    b = r"ꜥꜣḫẖꞽḥḤḪšŠṯṮḏḎꜥꜣḫꞼH̱nm"
    au = from_unicode(a)
    bu = from_unicode(b)
    print(au)
    print(bu)
    assert au == bu


def test_lcase():
    """Tests case changes."""
    a = r"ꜤꜢH̱ḪH"
    b = r"ꜥꜣẖḫh"
    au = from_unicode(a)
    bu = from_unicode(b)
    assert au.lower() == bu

def test_translit_output():
    a = "A1@$()Dd in sxty pn [S]&&"
    au = from_transliteration(a)
    b = au.to_transliteration()
    assert a == b

def test_replace():
    a = r"pu̯ pi̯ pʾ pï z"
    au = from_unicode(a)
    bu = from_unicode(r"pw pj pʾ pï z")
    cu = from_unicode(r"pu̯ pi̯ pꜣ pï z")
    du = from_unicode(r"pu̯ pi̯ pʾ py z")
    eu = from_unicode(r"pu̯ pi̯ pʾ pï s")
    fu = from_unicode(r"pw pj pꜣ py s")

    assert au.filter(UmFilter.REPLACE_INVERTED_BREVES) == bu
    assert au.filter(UmFilter.REPLACE_UNCERTAIN_CONSONANT) == cu
    assert au.filter(UmFilter.REPLACE_I_WITH_DIAERESIS) == du
    assert au.filter(UmFilter.REPLACE_Z) == eu
    assert au.filter(UmFilter.REPLACE_ALL) == fu


def test_mix_with_hieroglyphs():
    a = r"nṯr ꜥꜣ nb pt 𓇯👨‍👩‍👦"
    au = from_unicode(a)
    print(au)
    assert au.to_unicode() == a

def test_z():
    a0 =  from_unicode("Z")
    a = from_unicode("S", UmImport.S_FOR_Z)
    b = from_umschrift_ttn("c", UmImport.S_FOR_Z)
    c = from_trlit_cg_times("4", UmImport.S_FOR_Z)
    d = from_trlit_cg_times_2023("4", UmImport.S_FOR_Z)
    e = from_transliteration("%", UmImport.S_FOR_Z)
    assert a0 == a == b == c == d == e
def test_export_jj():
    a0 =  from_unicode("Imny Y")
    b = a0.to_unicode()
    c = a0.to_unicode(UmExport.JJ_FOR_DOUBLE_YOD)
    assert b == "Imny Y"
    assert c == "Imnjj Jj"    
def test_export_j():
    a0 =  from_unicode("Ꞽmny Yꞽ")
    b = a0.to_unicode()
    c = a0.to_unicode(UmExport.J_FOR_YOD + UmExport.JJ_FOR_DOUBLE_YOD)
    assert b == "Ꞽmny Yꞽ"
    assert c == "Jmnjj Jjj"  
def test_export_z():
    a0 =  from_unicode("sSzZ")
    b = a0.to_unicode()
    c = a0.to_unicode(UmExport.Z_FOR_S_AND_S_FOR_S_ACUTE)
    d = a0.to_transliteration(UmExport.Z_FOR_S_AND_S_FOR_S_ACUTE)
    assert b == "sSzZ"
    assert c == "śŚsS"
    assert d == "cCs%"

def test_export_k_dot():
    a0 =  from_unicode("qnbt Qnbt")
    b = a0.to_unicode()
    c = a0.to_unicode(UmExport.K_WITH_DOT)
    d = a0.to_transliteration(UmExport.K_WITH_DOT)
    e = a0.to_transliteration(UmExport.Z_FOR_S_AND_S_FOR_S_ACUTE)
    assert b == "qnbt Qnbt"
    assert c == "ḳnbt Ḳnbt" 
    assert d == "qnbt Qnbt"     
    assert e == "onbt Onbt"         
