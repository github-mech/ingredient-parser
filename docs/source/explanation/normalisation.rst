.. currentmodule:: ingredient_parser.en.preprocess

Sentence Normalisation
======================

Normalisation is the process of transforming the sentences to ensure that particular features of the sentence have a standard form. This pre-process step is there to remove as much of the variation in the data that can be reasonably foreseen, so that the model is presented with tidy and consistent data and therefore has an easier time of learning or labelling.

The :class:`PreProcessor` class handles the sentence normalisation for us.

.. code:: python

    >>> from Preprocess import PreProcessor
    >>> p = PreProcessor("1/2 cup orange juice, freshly squeezed")
    >>> p.sentence
    '0.5 cup orange juice, freshly squeezed'

The normalisation of the input sentence is done immediately when the :class:`PreProcessor` class is instantiated. The :func:`_normalise` method of the :class:`PreProcessor` class is called, which executes a number of steps to clean up the input sentence.

.. literalinclude:: ../../../ingredient_parser/en/preprocess.py
    :pyobject: PreProcessor._normalise
    :dedent: 4

.. tip::

    By setting ``show_debug_output=True`` when instantiating the :class:`PreProcessor` class, the sentence will be printed out at each step of the normalisation process.

Each of the normalisation functions are detailed below.


``_replace_en_em_dash``
^^^^^^^^^^^^^^^^^^^^^^^

En-dashes and em-dashes are replaced with hyphens.

.. literalinclude:: ../../../ingredient_parser/en/preprocess.py
    :pyobject: PreProcessor._replace_en_em_dash
    :dedent: 4


``_replace_html_fractions``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fractions represented by html entities (e.g. 0.5 as ``&frac12;``) are replaced with Unicode equivalents (e.g. ½). This is done using the standard library :func:`html.unescape` function.

.. literalinclude:: ../../../ingredient_parser/en/preprocess.py
    :pyobject: PreProcessor._replace_html_fractions
    :dedent: 4


``_replace_unicode_fractions``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fractions represented by Unicode fractions are replaced a textual format (.e.g ½ as 1/2), as defined by the dictionary in this function. The next step (``_replace_fake_fractions``) will turn these into decimal numbers.

We have to handle two cases: where the character before the unicode fraction is a hyphen and where it is not. In the latter case, we want to insert a space before the replacement so we don't accidentally merge with the character before. However, if the character before is a hyphen, we don't want to do this because we could end up splitting a range up.

.. literalinclude:: ../../../ingredient_parser/en/_constants.py
    :lines: 197-233

.. literalinclude:: ../../../ingredient_parser/en/preprocess.py
    :pyobject: PreProcessor._replace_unicode_fractions
    :dedent: 4

``combine_quantities_split_by_and``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fractional quantities split by 'and' e.g. 1 and 1/2 are converted to the format described in `_identify_fractions`_.

A regular expression is used to find these in the sentence.

.. literalinclude:: ../../../ingredient_parser/en/_regex.py
    :lines: 60-62

.. literalinclude:: ../../../ingredient_parser/en/_utils.py
    :pyobject: combine_quantities_split_by_and


``_identify_fractions``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fractions represented in a textual format (e.g. 1/2, 3/4) are identified and modified so that they survive tokenisation as a single token.
A regular expression is used to find these in the sentence. The regular expression also matches fractions greater than 1.

For fractions less than 1, the foward slash is replaced by ``$`` and a ``#`` is prepended e.g. #1$2 for 1/2.

For fractions greater than 1, the foward slash is replaced by ``$`` and a ``#`` is inserted between the integer and the fraction e.g. 2#3$4 for 2 3/4.

.. literalinclude:: ../../../ingredient_parser/en/_regex.py
    :lines: 7-10

.. literalinclude:: ../../../ingredient_parser/en/preprocess.py
    :pyobject: PreProcessor._identify_fractions
    :dedent: 4


``_split_quantity_and_units``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A space is enforced between quantities and units to make sure they are tokenized to separate tokens. If an quantity and unit are joined by a hyphen, this is also replaced by a space. This also takes into account certain strings that aren't technically units, but we want to treat in the same way here.

.. literalinclude:: ../../../ingredient_parser/en/_regex.py
    :lines: 15-35

.. literalinclude:: ../../../ingredient_parser/en/preprocess.py
    :pyobject: PreProcessor._split_quantity_and_units
    :dedent: 4


``_remove_unit_trailing_period``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Units with a trailing period have the period removed. This is only done for a subset of units where this has been observed.

.. literalinclude:: ../../../ingredient_parser/en/preprocess.py
    :pyobject: PreProcessor._remove_unit_trailing_period
    :dedent: 4


``replace_string_range``
^^^^^^^^^^^^^^^^^^^^^^^^^

Ranges are replaced with a standardised form of X-Y. The regular expression that searches for ranges in the sentence matches anything in the following forms:

* 1 to 2
* 1- to 2-
* 1 or 2
* 1- to 2-

where the numbers 1 and 2 represent any decimal value.

The purpose of this is to ensure the range is kept as a single token.

.. literalinclude:: ../../../ingredient_parser/en/_regex.py
    :lines: 37-58

.. literalinclude:: ../../../ingredient_parser/en/_utils.py
    :pyobject: replace_string_range

``_replace_dupe_units_ranges``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ranges where the unit is given for both quantities are replaced with the standardised range format, e.g. 5 oz - 8 oz is replaced by 5-8 oz. Cases where the same unit is used, but in a different form (e.g. 5 oz - 8 ounce) are also considered for the unit synonyms defined in ``UNIT_SYNONYMS``.

.. literalinclude:: ../../../ingredient_parser/en/_constants.py
    :lines: 404-415

.. literalinclude:: ../../../ingredient_parser/en/_regex.py
    :lines: 64-87

.. literalinclude:: ../../../ingredient_parser/en/preprocess.py
    :pyobject: PreProcessor._replace_dupe_units_ranges
    :dedent: 4

``_merge_quantity_x``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Merge quantities followed by an "x" into a single token, for example:

* 1 x -> 1x
* 0.5 x -> 0.5x

.. literalinclude:: ../../../ingredient_parser/en/_regex.py
    :lines: 89-98

.. literalinclude:: ../../../ingredient_parser/en/preprocess.py
    :pyobject: PreProcessor._merge_quantity_x
    :dedent: 4

``_collapse_ranges``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Remove any white space surrounding the hyphen in a range

.. literalinclude:: ../../../ingredient_parser/en/_regex.py
    :lines: 101-105

.. literalinclude:: ../../../ingredient_parser/en/preprocess.py
    :pyobject: PreProcessor._collapse_ranges
    :dedent: 4


``_singlarise_unit``
^^^^^^^^^^^^^^^^^^^^

Units are made singular using a predefined list of plural units and their singular form.

This step is actually performed after tokenisation (see :doc:`Extracting the features <features>`) and we keep track of the index of each token that has been singularised. This is so we can automatically re-pluralise only the tokens that were singularised after the labelling by the model.

.. literalinclude:: ../../../ingredient_parser/en/_constants.py
    :lines: 6-124
