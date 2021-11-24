import com.pack.utils.ReaderUtils;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.Tokenizer;
import org.apache.lucene.analysis.standard.StandardTokenizer;
import org.apache.lucene.analysis.synonym.SynonymGraphFilter;
import org.apache.lucene.analysis.synonym.SynonymMap;
import org.apache.lucene.util.CharsRef;

import java.util.List;

public class SynonymAnalyzer extends Analyzer {

    @Override
    protected TokenStreamComponents createComponents(String s) {
        SynonymMap.Builder builder=new SynonymMap.Builder(true);
        List<List<String>> synonyms = ReaderUtils.readSynonyms("./var/solr/data/text_search_core/config/synonyms.txt");
        synonyms.stream().forEach(el->el.stream().forEach(syn->syn.trim()));
        addSynonyms(builder, synonyms);
        words.forEach(el -> el.forEach(initial_word -> initial_word.forEach{synonym -> {
                    builder.add(new CharsRef(initial_word), new CharsRef(synonym), false);
        };);
        SynonymMap synonymMap = builder.build();
        Tokenizer tokenizer = new StandardTokenizer();
        TokenStream filter = new SynonymGraphFilter(tokenizer, synonymMap, true);
        return new TokenStreamComponents(tokenizer, filter);
    }
}