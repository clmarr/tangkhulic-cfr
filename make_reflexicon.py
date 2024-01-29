import sys

#for building reflex lexicon for a specific language column in the .tsv file
# pass the column title as the second argumentǃ
LANG = sys.argv[1]
EMPTY_INDIC = "-"
TSV_LOC = "ptk-"+LANG.lower()+".tsv"
PH_DELIM = " "

OUTFILE_LOC = LANG+"-lexicon.txt"

DIACRITS = ["ʷ","ʰ"]
DIGRAPHS = {"ts": "t͡s", "aa": "aː", "uu": "uː"}

def tokenize_phones (joined_str):
    ph_list = []
    js_left = ""+joined_str
    while len(js_left) > 0:
        if len(js_left) > 1:
            if js_left[0:2] in DIGRAPHS.keys():
                ph_list += [DIGRAPHS.get(js_left[0:2]) ]
                js_left = js_left[2:]
                continue
        if len(ph_list) > 0:
            if js_left[0:1] in DIACRITS:
                ph_list[-1] += js_left[0]
                js_left = js_left[1:]
        ph_list += [js_left[0]]
        js_left = js_left[1:]
    return ph_list

file_lines = ""
with open(TSV_LOC) as file:
    file_lines = [  ln.split('\t')
            for ln in file.readlines() if '[' not in ln]
    # filter out the one linethat is "ruul\t['ke','phwi'] for Kachai, as this is not a real etymology.

with open(OUTFILE_LOC,'w') as file:
    file.write("$Proto-Tangkhulic?, "+LANG+"\n")

    # write each line.
    for et in file_lines:
        headword = tokenize_phones(et[0])
        reflex = tokenize_phones(et[1])

       # cmt = "$"+et[GLOSS_COL]+": "+headword+" > ... > "+reflex
            # compose comment to indicate the gloss, which is found in the first column (presently)
            # .. and the etymology

        # when writing line, impose spacing rules on phonemes in headword and reflex
        list_to_join = headword + [","] + reflex
        file.write(PH_DELIM.join(list_to_join)
                   #+ " " + cmt + "\n")
                   )
