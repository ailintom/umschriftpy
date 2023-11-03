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
    assert ([item.to_unicode() for item in name_list_sorted]) == ['ꜣw-ꞽb', 'ꜥꜣ-ptḥ', 'nfr-ḥtp', 'ḏḥwtꞽ-nfr']
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

    name_list_from_sqlite =  [from_pseudo(r) for r in result]
    assert  [i.to_unicode() for i in name_list_from_sqlite] == ['ꜣw-ꞽb', 'ꜥꜣ-ptḥ', 'nfr-ḥtp', 'ḏḥwtꞽ-nfr']
        


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
    
    assert au==bu[4:] and bu.find(au)==4
def test_transliteration():
    """Tests Transliteration imports."""      
    a = r"~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:||ZXCVBNM<>?qwertyuiop[]asdfghjkl;'\\zxcvbnm,./"
    b = r"~HḤḪH̱SŠTṮ()DḎḲWERṯYUꞼQP{}ꜣšḏFGḥJKL:||ZẖŚh̭BNM<>?ḳwertyuꞽqp[]ꜥsdfghjkl;'\\zḫśṱbnm,./"

    au = from_transliteration(a)
    bu = from_unicode(b)
    print (au)
    print(bu)
    assert au==bu  
def test_trlitcgtimes():
    """Tests trlit_cg_times imports."""      
    a = r"~@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:||ZXCVBNM<>?qwertyuiop[]asdfghjkl;'\\zxcvbnm,./"
    b = r"~@#$%^&*()_+ḲWERṯYUꞼQP{}ꜣšḏFGḥJK⸥:||ZẖŚṰBNM<>?ḳwertyuꞽqp[]ꜥsdfghjkl;'\\zḫśṱbnm,./"

    au = from_trlit_cg_times(a)
    bu = from_unicode(b)
    print (au)
    print(bu)
    assert au==bu      
def test_trlitcgtimes2023():
    """Tests trlit_cg_times 2023 imports."""      
    a = r"~@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:||ZXCVBNM<>?qwertyuiop[]asdfghjkl;'\\zxcvbnm,./"
    b = r"⸢č⸣č̣%H̭&ʾ()_+ḲWERṯïUꞼQP{}ꜣšḏFGḥJK⸥:||ZẖŚṰBNM⟨⟩?ḳwertyh̭ꞽqp[]ꜥsdfghjkl;'\\zḫśṱbnm,./"

    au = from_trlit_cg_times_2023(a)
    bu = from_unicode(b)
    print (au)
    print(bu)
    assert au==bu      
def test_unicode(): 
    """Tests IFAO Unicode imports."""          
    a = r"ʿȝḫẖỉḥḤḪšŠṯṮḏḎʿȝḫỈH̱nm"
    b = r"ꜥꜣḫẖꞽḥḤḪšŠṯṮḏḎꜥꜣḫꞼH̱nm"
    au = from_unicode(a)
    bu = from_unicode(b)
    print (au)
    print(bu)
    assert au==bu  
def test_lcase():
    """Tests case changes."""          
    a = r"ꜤꜢH̱ḪH"
    b = r"ꜥꜣẖḫh"
    au = from_unicode(a)
    bu = from_unicode(b)
    assert au.lower()==bu   
def test_replace():
    a = r"pu̯ pi̯ pʾ pï"
    au = from_unicode(a)
    bu = from_unicode(r"pw pj pʾ pï")
    cu = from_unicode(r"pu̯ pi̯ pꜣ pï")
    du = from_unicode(r"pu̯ pi̯ pʾ py")


    assert au.filter(UmFilter.REPLACE_INVERTED_BREVES)==bu  
    assert au.filter(UmFilter.REPLACE_UNCERTAIN_CONSONANT)  ==cu  
    assert au.filter(UmFilter.REPLACE_I_WITH_DIAERESIS)  ==du 