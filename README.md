# umschriftpy
A Python library for dealing with Egyptological transliteration/transcription.
This library is made for standardizing Egyptological transliteration/transcription with the aim of processing data stemming from digital project with different approaches to Egyptological transliteration/transcription.
`umschriftpy` should be able to import Egyptological transliteration/transcription entered in different flavours of Unicode, as well as in conventional fonts Umschrift_TTn, Transliteration, and Trlit_CG Times and using different Egyptological conventions.
One particultar application it was developed for is matching entries in across different databases.
The Leiden Unified Transliteration/Transcription https://www.iae-egyptology.org/the-leiden-unified-transliteration serves as the basis for normalisation.

It aims to be ported to other common programming languages used in the development of Egyptological applications. 

## Usage

The package provides a class for working with Egyptological transliteration/transcription named `UmschString` and methods for creating objects of this class from srtings.
In order to create an `UmschString` object you can use one of the folowing methods: 
- `from_unicode` loads Unicode-formatted strings
- `from_umschrift_ttn` loads strings formatted with Umschrift_TTn v3.0 font (https://wwwuser.gwdg.de/~lingaeg/lingaeg-stylesheet.htm)
- `from_trlit_cg_times` loads strings formatted with the 2023 version of the Trlit_CG Times font (https://dmd.wepwawet.nl/fonts.htm https://oeb.griffith.ox.ac.uk/fonts.aspx)
- `from_trlit_cg_times_2023` loads strings formatted with the pre-2023 version of the Trlit_CG Times font
- `from_transliteration` loads strings formatted with Transliteration font (CCER), downloadable from the link above

The `UmschString` object have export methods and support some of the Python string methods (`upper`, `lower`, `index`, `find`, `replace`, `endswith`, `startswith`)
Data can be outputted to string using the `to_unicode` method. By default this method uses the Leiden Unified Transliteration/Transcription, however divergences can be set up by optional flags: 
`K_WITH_DOT` uses ḳ and Ḳ for q and Q
`J_FOR_YOD`  uses j and J for ꞽ and Ꞽ
`JJ_FOR_DOUBLE_YOD`  uses jj and Jj for y and Y as well as for ï and Ï
`SUPRESS_I_WITH_DIAERESIS`  uses y and Y for ï and Ï
Flags can be combined using the bitwise OR `|` operator

Example: 
```
uma = umschriftpy.from_trlit_cg_times("Htp dj nsw Wp-WAwt nb tA Dsr dj=f prt-xrw (m) t Hnqt")
uma_lower = uma.lower()
uma_replaced = umalower.replace(umschriftpy.from_trlit_cg_times("nsw"), umschriftpy.from_trlit_cg_times("njswt"))
print(uma_replaced.to_unicode())
print(uma_replaced.to_unicode(umschriftpy.ExportRules.K_WITH_DOT))

```


## Disclaimer
The current preliminary version is merely a proof of concept. It is not yet ready for use. 

The package is developed as part of the project “Altägyptische Titel in amtlichen und familiären Kontexten, 2055-1352 v. Chr.”, funded by the Fritz Thyssen Foundation.