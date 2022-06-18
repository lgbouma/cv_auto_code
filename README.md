This script creates tex files with lists of publications from ADS libraries. The lists will have your name bolded and include links to the ADS pages for each of your papers.

To use, you will first need to edit three files:

1. `my_key.txt` -- your [ADS API key](https://ui.adsabs.harvard.edu/user/settings/token). You need this to access the API, even for public libraries.
2. `my_names.txt` -- how your name is listed in bibtex entries. This will then enable the script to bold your name. Typically this is in the form "{LastName}, FirstName". Put only one name on each line.
3. `my_libraries.txt` -- each line should have an ADS library id, followed by the latex file you wish to output to.

This will create as many tex files as lines in `my_libraries.txt`. You can then use the `\input{}` command in your CV tex file to put these files within your cv.

**Pro-tip** - You can run this script every time you compile your CV by doing the following:
1. Before `\begin{document}` in your CV tex file, insert `\immediate\write18{./run_cv_gen.sh}`. (You might need to make the shell file executable)
2. When you call pdflatex, use the flag `--shell-escape`.
