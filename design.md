(id, key, <value type>, value)

id - unique numbering on each instance
key - property name 
<value type> - value type( see below)
value - property value 

value type must be one of:
    bool (python native)
    int (python native)
    string (python native)
    ref (referenc to other instance)
    mref (entry of reference set)

special id
<special> "Book", <id-0>
<special> "Book", <id-1>
<special> "Tag", <id-0>
... => constructor to omit 'path'
id-0 is 'init' object, meta thing, world, root, class manager, whatever..
(<id-0>, "Book", mref, <id-1>)
(<id-0>, "Book", mref, <id-2>)
(<id-0>, "Book", mref, <id-3>)
(<id-0>, "Book", mref, <id-4>)
(<id-0>, "Tag", mref, <id-5>)
(<id-0>, "Tag", mref, <id-6>)
(<id-0>, "Tag", mref, <id-7>)
....


concrete example for book db

!! we may have very same two books, so using isbn as id is a WRONG idea.

("Book", <id-0>, "title", "this is title")
("Book", <id-0>, "isbn", "00000000")
("Book", <id-0>, "tags", <id-3>) # it is "dangling". reference it, but not begin referenced.
("Book", <id-0>, "tags", <id-4>)
("Tag", <id-3>, "name", "geek") 
("Tag", <id-4>, "name", "cooking")
("Tag", <id-4>, "books", <id-0>) #is this right idea? => y. need tough maintenamce

issue:
    How to find "dangling"/orphan entry?
    nested tag.

nested tag 

an idea... not good
("Tag", <id-3>, "name", "meat") 
("Tag", <id-3>, "/Tag", <id-4>)
("Tag", <id-4>, "name", "chicken")
("Tag", <id-4>, "parent", <id-3>) #ugh!

another idea for nested tag
("Tag", <id-3>, "name", "meat") 
("Tag", <id-4>, "name", "meat/chicken") #wrong. giving special meaning to value 

yet another idea for nested tag 
("Tag", <id-3>, "name", "meat")
("Tag", <id-3>, "subtag", <id-4>) #mref
("Tag", <id-3>, "subtag", <id-5>)
("Tag", <id-3>, "subtag", <id-6>)
("Tag", <id-4>, "name", "chicken")
("Tag", <id-5>, "name", "pork")
("Tag", <id-6>, "name", "beaf")

issue:
    How to get parent => have a "parent", need ref/mref(multiple ref)
    value types. How to distinguish between int value and <id> => we type value


or we can go more "relational" on book-tag feature.
This forces us to "join".... which I do not want.

("Book", <id-0>, "title", "this is title")
("Book", <id-0>, "isbn", "00000000")
("Tag", <id-3>, "name", "geek") 
("Tag", <id-4>, "name", "cooking")

("Relation", <id-5>, "Left", <id-0>) #relation "object" MxN
("Relation", <id-5>, "Right", <id-3>) 

("Relation", <id-6>, "Left", <id-0>)
("Relation", <id-6>, "Right", <id-4>)


discussion:
 * trade off against ORM+SQLdb
  * human readable datafile
   * There is sql with csv? should be checked out.
   * can export/import. not csv as storage
 * why not pickle?
  * not readable from non-python
 * why not xml?
  * ref, flexibility
 * why not yaml?
  * not sure.
  * & and * are useful.
   * Yes! PyYaml supports it!
    * the point is, how to generate name for &/*
     * they do automatically.
'''python
f = "fooo"
zm = [f, f]

print yaml.dump([zm, zm])
'''
would give
'''
 - &id001 [fooo, fooo]
 - *id001
'''
   * tag (typing) is also supported
    * we need validator?
 * Is worth for sweat and bugs?
  * not sure.
 * Is this fun?
  * yes

We use yaml.
questions are:
    How to map regular objects into list+str+int combination? => Proxy

Should write sample yamls first.


We have yaml samples now.
 * time to validate it with schema
   * Rx: too hard to understand.
   * Kwalify. 

We have schema (kw-schema.py)
 * Yes. It is valid.

Customizing loader.
 * pyyaml add_constructor and add_path_resolver are not 
  flexible enough.
 * visit.py, overtaking visitor.
   * defining path is "duplicated" with schema
   * why not load schema?
     * Does that mean defining python class in yaml?

 * XPath
   * location-path = location-step with sep of '/'
   * location-step = axis, node-test, predicate
   * full-sample
     * /child::A/child::B/child::C
     * child::A/descendant-or-self::node()/child::B/child::*[1]
   * axis 
     * child 軸 (default)
     * attribute軸
     * descendant-or-self軸
     * self軸
     * parent軸
   * context
     * child::  省略して何も書かない
     * attribute:: @
     * /descendant-or-self::node()/ 	//
     * self::node() .
     * parent::node() ..
   * predicate = []
     * example  //a[@href='help.php']

> 先の例では述語の数は1つであったが、
> ロケーションパスを構成するロケーションステップごとに、
> 複数の述語を指定することができる。 すなわち、
> 絞り込み条件を複数重ねて指定することができる。 
> 指定できる述語の数に制限は無い。
> 
> 述語は、その述語を含むロケーションステップの
> コンテクストを変更することは無い。 その直前の
> ノードテストで指定されたノード集合が
> そのロケーションステップのコンテクストであり、
> 述語が指定されることでコンテクストが変更されることは無い。

> 複雑な例を示す。
> 
>     //a[@href='help.php'][name(..)='div'][../@class='header']/@target
> 
> この例は、a 要素の target 属性の値を指定する。 ただしこのXPath式の最初のロケーションステップには3つの述語が記述されており、a 要素のうち
> 
>     a 要素の href 属性の値が 'help.php' であり、
>     且つ、a 要素の親要素の要素名が div であり、
>     且つ、親要素 (div) の class 属性の値が 'header' である、
> 
> a 要素のみが、最初のロケーションステップの指定対象となる。 最終的には、最初のロケーションステップで絞り込まれて指定対象となった a 要素の target 属性が指定されることになる。
> 



XPathはData ModelとしてDOMを持っている。
そして、ツリー構造に関して制約がある。
これをYAMLが満たしていない。

a) ドキュメント順
b) 親ノードの単一性


a) ドキュメント順

辞書に対してドキュメント順が定義されない可能性がある。

> ドキュメント内のすべてのノードで定義する
> ドキュメント順という順序付けがある。
> これは一般エンティティの展開後に、ドキュメントの
> XML 表現において各ノードの XML 表現の最初の文字が
> 現れる順序を表したものである。 従ってルートノードが
> 最初のノードになる。 エレメントノードは、
> それ自身の子よりも先になる。 
> このようにドキュメント順は、
> (エンティティを展開した後で) XML 内で
> エレメントノードのスタートタグを記述する順序に
> 従ってエレメントノードを順序付けしたものである。 
> エレメントのアトリビュートノードと
> ネームスペースノードは、そのエレメントの子ノードより
> も先になる。 ネームスペースノードは
> アトリビュートノードよりも先になるように定義する。 
> ネームスペースノードの相対的な順序は、
> 実装により異なる。 アトリビュートノードの
> 相対的な順序も実装によって異なる。
> 逆ドキュメント順はドキュメント順を逆にしたものである。


b) 親ノードの単一性

参照(&/*)が同値なものの省略記法でならそれを
展開したものに適応すればよい。が、同一
なものに関する記法である場合、無理が生じる。

あるノードにとって、親ノードは１つだけ。
> ルートノードとエレメントノードは、
> 子ノードを順序付けたリストを持つ。
> ノードが子ノードを共有することはない。 
> 従って異なる２つのノードがある場合、
> 片方のノードの子ノードはすべて、
> もう１つのノードの子ノードとは異なる。 
> ルートノードを除くすべてのノードは、
> 必ず親ノードを１つ持つ。
> 親ノードになるのはルートノードか
> エレメントノードのどちらかである。 
> ルートノードまたはエレメントノードは、
> それぞれが持つ個々の子ノードからみると
> 親ノードになる。 ノードの子孫ノードとは、
> そのノードの子ノード、および子ノードの子孫ノードになる。 

