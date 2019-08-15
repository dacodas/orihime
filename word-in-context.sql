WITH RECURSIVE WordInContext(id, parent, reading, begin, end, contents) AS (
    SELECT orihime_text.id, NULL, "", 0, 0, orihime_text.contents
    FROM orihime_text
    WHERE orihime_text.id = %s
    UNION ALL
    SELECT orihime_word.definition_id,
           WordInContext.id,
           orihime_word.reading,
           orihime_wordrelation.begin,
           orihime_wordrelation.end,
           destination.contents
    FROM orihime_text AS source,
         WordInContext
    INNER JOIN orihime_wordrelation ON orihime_wordrelation.text_id = source.id
    INNER JOIN orihime_word ON orihime_word.id = orihime_wordrelation.word_id
    INNER JOIN orihime_text AS destination ON destination.id = orihime_word.definition_id
    WHERE source.id = WordInContext.id
  )
SELECT * from WordInContext;
