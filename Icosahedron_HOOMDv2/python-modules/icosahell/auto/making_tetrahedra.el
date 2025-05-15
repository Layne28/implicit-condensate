(TeX-add-style-hook
 "making_tetrahedra"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "10pt" "a4paper")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("appendix" "toc" "page") ("cite" "sort")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10"
    "inputenc"
    "amsmath"
    "amsfonts"
    "amssymb"
    "graphicx"
    "caption"
    "subcaption"
    "epstopdf"
    "abstract"
    "appendix"
    "cite"
    "hyperref")
   (TeX-add-symbols
    '("dd" 0)
    '("dotprod" 2)
    '("bigO" 2)
    '("bvec" 1)
    '("half" 0)))
 :latex)

