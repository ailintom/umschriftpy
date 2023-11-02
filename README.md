# umschrift*py*
A Python 3 library for dealing with Egyptological transliteration/transcription.

## Description

This library is made for standardising Egyptological transliteration/transcription with the aim of processing data from digital projects with different approaches to Egyptological transliteration/transcription. `umschriftpy` should be able to import Egyptological transliteration/transcription entered in different Unicode flavours, as well as in the conventional fonts Umschrift_TTn, Transliteration and Trlit_CG Times, and using different Egyptological conventions. One particular application for which it was developed is the matching of entries in different databases. The Leiden Unified Transliteration/Transcription https://www.iae-egyptology.org/the-leiden-unified-transliteration serves as the basis for the normalisation.

It is intended to be ported to other common programming languages used in the development of Egyptological applications.

## Usage

The package provides a class for working with Egyptological transliteration/transcription called `UmschString` and methods for creating objects of this class from strings.
To create an `UmschString` object you can use one of the following methods:
- `from_unicode` loads Unicode-formatted strings
- `from_umschrift_ttn` loads strings formatted with Umschrift_TTn v3.0 font (https://wwwuser.gwdg.de/~lingaeg/lingaeg-stylesheet.htm)
- `from_trlit_cg_times_2023` loads strings formatted with the 2023 version of the Trlit_CG Times font (https://dmd.wepwawet.nl/fonts.htm https://oeb.griffith.ox.ac.uk/fonts.aspx)
- `from_trlit_cg_times` loads strings formatted with the pre-2023 version of the Trlit_CG Times font
- `from_transliteration` loads strings formatted with Transliteration font (CCER), downloadable from the link above

The `UmschString` objects have export methods for outputting strings and support some of the Python string methods (`upper`, `lower`, `index`, `find`, `replace`, `endswith`, `startswith`)
Data can be cleaned up using the `filter` method, with filtering options set by flags:
`UmFilter.MORPH` removes morphological markers `. : ·`
`UmFilter.SUFF_PRON` removes suffix pronoun separators `⸗`
`UmFilter.BRACKETS` removes brackets `⸢ ⸣ ⟨ ⟩ ( ) [ ] < > { } |`
`UmFilter.PUNCT` removes punctuation `? ! " , .`
`UmFilter.ALL` removes all of the above
`UmFilter.DIGITS` removes all digits
`UmFilter.FACULTATIVE` removes parentheses and all signs enclosed in parentheses
`UmFilter.LOWER` converts all transliteration/transcription to lower case
`UmFilter.HYPHENS` replaces all hyphens with spaces

Data can be output to string using the `to_unicode` method. By default this method uses the Leiden Unified Transliteration/Transcription, but deviations  can be set up by optional flags: 
`UmExport.K_WITH_DOT` uses ḳ and Ḳ for q and Q
`UmExport.J_FOR_YOD`  uses j and J for ꞽ and Ꞽ
`UmExport.JJ_FOR_DOUBLE_YOD`  uses jj and Jj for y and Y as well as for ï and Ï
`UmExport.SUPRESS_I_WITH_DIAERESIS`  uses y and Y for ï and Ï
Flags can be combined using the bitwise OR `|` operator

## Examples: 
```python
from umschriftpy import *

#       CONVERSION

# imports a Trlit_CG Times string
uma = from_trlit_cg_times(
    "Htp dj nsw Wp-WAwt nb tA Dsr dj=f prt-xrw (m) t Hnqt")
uma_lower = uma.lower()  # converts it to lower cases
uma_replaced = uma_lower.replace(from_trlit_cg_times(
    "nsw"), from_trlit_cg_times("njswt"))  # replaces a word
print(uma_replaced.to_unicode())  # exports to Unicode
# >>> ḥtp dꞽ nꞽswt wp-wꜣwt nb tꜣ ḏsr dꞽ⸗f prt-ḫrw (m) t ḥnqt
# exports to Unicode with a special option (ḳ instead of q)
print(uma_replaced.to_unicode(UmExport.K_WITH_DOT))
# >>> ḥtp dꞽ nꞽswt wp-wꜣwt nb tꜣ ḏsr dꞽ⸗f prt-ḫrw (m) t ḥnḳt

#       CLEANING UP STRINGS FOR COMPARISON

a = from_umschrift_ttn("O#.tj-o-jj#")  # imports an Umschrift_TTn string
print(a.to_unicode())
# >>> Ḥꜣ.tꞽ-ꜥ-yꜣ
b = from_unicode("ḥꜣtꞽ ꜥ yꜣ")  # imports an Unicode string
print(b.to_unicode())
# >>> ḥꜣtꞽ ꜥ yꜣ
# the strings are different because of different punctuation, lowercase and uppercase letters
print(a == b)
# >>> False
a_filtered = a.filter(UmFilter.ALL | UmFilter.HYPHENS | UmFilter.LOWER)
b_filtered = b.filter(UmFilter.ALL | UmFilter.HYPHENS |
                      UmFilter.LOWER)  # filters strings
print(a_filtered == b_filtered)  # filtered strings are now equal
# >>> True
print(a_filtered.to_unicode())
# >>> ḥꜣtꞽ ꜥ yꜣ

#       SORTING

# inputting several names as a list
name_list = [from_transliteration("nfr-Htp"), from_transliteration(
    "aA-ptH"), from_transliteration("DHw.tj-nfr"), from_transliteration("Aw-jb")]
# filtering list values
name_list_filtered = [item.filter(UmFilter.ALL | UmFilter.LOWER)
                      for item in name_list]
# using a standard Python function to sort items
name_list_sorted = sorted(name_list_filtered)
# outputting the sorted list as Unicode
print([item.to_unicode() for item in name_list_sorted])
# >>> ['ꜣw-ꞽb', 'ꜥꜣ-ptḥ', 'nfr-ḥtp', 'ḏḥwtꞽ-nfr']
```


## Disclaimer and acknowledgements
The current preliminary version is merely a proof of concept. It is not yet ready for use. 

The package is being developed as part of the project “Altägyptische Titel in amtlichen und familiären Kontexten, 2055-1352 v. Chr.”, funded by the Fritz Thyssen Foundation.