#!/usr/bin/env python3
"""Final batch to reach 500 Core Basic."""
import json, re
from pathlib import Path
ROOT = Path(__file__).parent.parent

NEW = [
  ["xin chào lại","Xin chào lại nhé.","また<ruby>会<rt>あ</rt></ruby>いましたね","また<ruby>会<rt>あ</rt></ruby>いましたね。","hello again","Hello again.","Greeting"],
  ["chào bạn","Chào bạn nhé.","やあ","やあ、こんにちは。","hi friend","Hi friend.","Greeting"],
  ["thật vậy","Thật vậy sao?","<ruby>本当<rt>ほんとう</rt></ruby>に?","<ruby>本当<rt>ほんとう</rt></ruby>に?","really?","Really?","Question"],
  ["thật ra","Thật ra tôi không biết.","<ruby>実<rt>じつ</rt></ruby>は","<ruby>実<rt>じつ</rt></ruby>は<ruby>知<rt>し</rt></ruby>りません。","actually","Actually I don't know.","Adverb"],
  ["có thể là","Có thể là vậy.","かもしれない","そうかもしれません。","could be","Could be.","Adverb"],
  ["bao gồm","Bao gồm thuế chưa?","<ruby>含<rt>ふく</rt></ruby>む","<ruby>税<rt>ぜい</rt></ruby><ruby>込<rt>こ</rt></ruby>みですか?","include","Tax included?","Verb"],
  ["loại bỏ","Loại bỏ phần thừa.","<ruby>取<rt>と</rt></ruby>り<ruby>除<rt>のぞ</rt></ruby>く","<ruby>余分<rt>よぶん</rt></ruby>な<ruby>部分<rt>ぶぶん</rt></ruby>を<ruby>取<rt>と</rt></ruby>り<ruby>除<rt>のぞ</rt></ruby>く。","remove","Remove the excess.","Verb"],
  ["thêm","Thêm một ít muối.","<ruby>足<rt>た</rt></ruby>す","<ruby>塩<rt>しお</rt></ruby>を<ruby>少<rt>すこ</rt></ruby>し<ruby>足<rt>た</rt></ruby>す。","add","Add some salt.","Verb"],
  ["bớt","Bớt cay nhé.","<ruby>少<rt>すく</rt></ruby>なめに","<ruby>辛<rt>から</rt></ruby>さを<ruby>少<rt>すく</rt></ruby>なめに。","reduce","Less spicy please.","Verb"],
  ["lớn","Cái này lớn quá.","<ruby>大<rt>おお</rt></ruby>きい","これは<ruby>大<rt>おお</rt></ruby>きすぎます。","big","This is too big.","Adjective"],
  ["nhỏ","Cỡ nhỏ thôi.","<ruby>小<rt>ちい</rt></ruby>さい","<ruby>小<rt>ちい</rt></ruby>さいサイズで。","small","Small size only.","Adjective"],
  ["vừa","Vừa đủ rồi.","ちょうどいい","ちょうどいいです。","just right","Just right.","Adjective"],
  ["hơn","Tốt hơn rồi.","より<ruby>良<rt>よ</rt></ruby>い","より<ruby>良<rt>よ</rt></ruby>くなりました。","more","Better now.","Adverb"],
  ["kém","Hơi kém một chút.","<ruby>少<rt>すこ</rt></ruby>し<ruby>劣<rt>おと</rt></ruby>る","<ruby>少<rt>すこ</rt></ruby>し<ruby>劣<rt>おと</rt></ruby>ります。","less","A little less.","Adverb"],
  ["bằng","Hai cái bằng nhau.","<ruby>同<rt>おな</rt></ruby>じ","<ruby>二<rt>ふた</rt></ruby>つは<ruby>同<rt>おな</rt></ruby>じです。","equal","Two are equal.","Adjective"],
  ["hơn nữa","Hơn nữa, trời còn mưa.","しかも","しかも、<ruby>雨<rt>あめ</rt></ruby>も<ruby>降<rt>ふ</rt></ruby>っています。","moreover","Moreover, it's raining.","Adverb"],
  ["tuy nhiên","Tuy nhiên tôi vẫn đi.","しかし","しかし、<ruby>行<rt>い</rt></ruby>きます。","however","However, I'll go.","Adverb"],
  ["vì vậy","Vì vậy tôi không đi.","だから","だから<ruby>行<rt>い</rt></ruby>きません。","therefore","So I won't go.","Adverb"],
  ["bởi vì","Bởi vì tôi mệt.","なぜなら","なぜなら<ruby>疲<rt>つか</rt></ruby>れたからです。","because","Because I'm tired.","Adverb"],
  ["mặc dù","Mặc dù mưa.","~なのに","<ruby>雨<rt>あめ</rt></ruby>なのに。","although","Although it rains.","Adverb"],
  ["nếu","Nếu rảnh, gọi tôi.","もし","もし<ruby>暇<rt>ひま</rt></ruby>なら、<ruby>電話<rt>でんわ</rt></ruby>して。","if","If you're free, call.","Adverb"],
  ["khi","Khi nào đến?","いつ","いつ<ruby>来<rt>き</rt></ruby>ますか?","when","When are you coming?","Adverb"],
  ["trong","Trong phòng có ai?","<ruby>中<rt>なか</rt></ruby>に","<ruby>部屋<rt>へや</rt></ruby>の<ruby>中<rt>なか</rt></ruby>に<ruby>誰<rt>だれ</rt></ruby>か?","inside","Anyone inside?","Adverb"],
  ["sau khi","Sau khi ăn xong.","<ruby>食<rt>た</rt></ruby>べた<ruby>後<rt>あと</rt></ruby>","<ruby>食<rt>た</rt></ruby>べた<ruby>後<rt>あと</rt></ruby>。","after","After eating.","Adverb"],
  ["trước khi","Trước khi đi ngủ.","<ruby>寝<rt>ね</rt></ruby>る<ruby>前<rt>まえ</rt></ruby>","<ruby>寝<rt>ね</rt></ruby>る<ruby>前<rt>まえ</rt></ruby>に。","before","Before sleeping.","Adverb"],
  ["mỗi ngày","Mỗi ngày tôi học.","<ruby>毎日<rt>まいにち</rt></ruby>","<ruby>毎日<rt>まいにち</rt></ruby><ruby>勉強<rt>べんきょう</rt></ruby>します。","every day","I study every day.","Time"],
  ["cả ngày","Cả ngày làm việc.","<ruby>一日中<rt>いちにちじゅう</rt></ruby>","<ruby>一日中<rt>いちにちじゅう</rt></ruby><ruby>仕事<rt>しごと</rt></ruby>。","all day","Work all day.","Time"],
  ["nửa ngày","Nửa ngày trôi qua.","<ruby>半日<rt>はんにち</rt></ruby>","<ruby>半日<rt>はんにち</rt></ruby><ruby>過<rt>す</rt></ruby>ぎた。","half day","Half day passed.","Time"],
  ["một lát","Đợi một lát.","ちょっと","ちょっと<ruby>待<rt>ま</rt></ruby>って。","a moment","Wait a moment.","Time"],
  ["lát nữa","Lát nữa gọi lại.","<ruby>後<rt>あと</rt></ruby>で","<ruby>後<rt>あと</rt></ruby>で<ruby>電話<rt>でんわ</rt></ruby>します。","later","Call you later.","Time"],
  ["dễ","Câu hỏi dễ.","<ruby>簡単<rt>かんたん</rt></ruby>","<ruby>簡単<rt>かんたん</rt></ruby>な<ruby>質問<rt>しつもん</rt></ruby>。","easy","Easy question.","Adjective"],
  ["ngon miệng","Chúc ngon miệng.","召し<ruby>上<rt>あ</rt></ruby>がれ","召し<ruby>上<rt>あ</rt></ruby>がれ。","enjoy meal","Enjoy your meal.","Greeting"],
  ["may mắn","Chúc may mắn.","<ruby>幸運<rt>こううん</rt></ruby>を","<ruby>幸運<rt>こううん</rt></ruby>を<ruby>祈<rt>いの</rt></ruby>る。","good luck","Good luck.","Greeting"],
  ["xin lỗi nhiều","Xin lỗi nhiều ạ.","<ruby>本当<rt>ほんとう</rt></ruby>にすみません","<ruby>本当<rt>ほんとう</rt></ruby>にすみません。","very sorry","I'm very sorry.","Greeting"],
  ["xin phép","Xin phép đi trước.","<ruby>失礼<rt>しつれい</rt></ruby>します","お<ruby>先<rt>さき</rt></ruby>に<ruby>失礼<rt>しつれい</rt></ruby>します。","excuse me","Excuse me, going first.","Greeting"],
  ["chờ chút","Chờ chút nhé.","ちょっと<ruby>待<rt>ま</rt></ruby>って","ちょっと<ruby>待<rt>ま</rt></ruby>って。","wait a bit","Wait a moment.","Greeting"],
  ["nói lại","Anh nói lại được không?","もう<ruby>一度<rt>いちど</rt></ruby>","もう<ruby>一度<rt>いちど</rt></ruby><ruby>言<rt>い</rt></ruby>って?","say again","Say again?","Verb"],
  ["nhỏ tiếng","Nói nhỏ tiếng thôi.","<ruby>小声<rt>こごえ</rt></ruby>で","<ruby>小声<rt>こごえ</rt></ruby>で<ruby>話<rt>はな</rt></ruby>す。","quietly","Speak quietly.","Adverb"],
  ["lớn tiếng","Đừng nói lớn tiếng.","<ruby>大声<rt>おおごえ</rt></ruby>で","<ruby>大声<rt>おおごえ</rt></ruby>を<ruby>出<rt>だ</rt></ruby>さないで。","loudly","Don't speak loudly.","Adverb"],
  ["chậm chậm","Chậm chậm thôi.","ゆっくり","ゆっくり。","slowly","Slowly.","Adverb"],
  ["vội","Đừng vội.","<ruby>急<rt>いそ</rt></ruby>がない","<ruby>急<rt>いそ</rt></ruby>がないで。","hurry","Don't hurry.","Verb"],
  ["nhường","Nhường ghế cho người già.","<ruby>譲<rt>ゆず</rt></ruby>る","<ruby>年配<rt>ねんぱい</rt></ruby>の<ruby>方<rt>かた</rt></ruby>に<ruby>席<rt>せき</rt></ruby>を<ruby>譲<rt>ゆず</rt></ruby>る。","yield","Yield seat to elderly.","Verb"],
  ["bay","Máy bay sắp bay.","<ruby>飛<rt>と</rt></ruby>ぶ","<ruby>飛行機<rt>ひこうき</rt></ruby>が<ruby>飛<rt>と</rt></ruby>ぶ。","fly","Plane is taking off.","Verb"],
  ["bơi","Tôi không biết bơi.","<ruby>泳<rt>およ</rt></ruby>ぐ","<ruby>泳<rt>およ</rt></ruby>げません。","swim","I can't swim.","Verb"],
  ["thấy","Thấy không?","<ruby>見<rt>み</rt></ruby>える","<ruby>見<rt>み</rt></ruby>えますか?","see","Can you see?","Verb"],
  ["tìm","Tôi tìm cái này.","<ruby>探<rt>さが</rt></ruby>す","これを<ruby>探<rt>さが</rt></ruby>しています。","look for","I'm looking for this.","Verb"],
  ["tìm thấy","Tôi tìm thấy rồi.","<ruby>見<rt>み</rt></ruby>つけた","<ruby>見<rt>み</rt></ruby>つけました。","found","I found it.","Verb"],
  ["mất","Tôi mất chìa khoá.","なくす","<ruby>鍵<rt>かぎ</rt></ruby>をなくしました。","lose","I lost my key.","Verb"],
  ["đặt tên","Đặt tên cho mèo.","<ruby>名前<rt>なまえ</rt></ruby>をつける","<ruby>猫<rt>ねこ</rt></ruby>に<ruby>名前<rt>なまえ</rt></ruby>をつける。","name","Name the cat.","Verb"],
  ["gọi","Gọi cho tôi.","<ruby>呼<rt>よ</rt></ruby>ぶ / <ruby>電話<rt>でんわ</rt></ruby>","<ruby>電話<rt>でんわ</rt></ruby>してください。","call","Call me.","Verb"],
  ["trả lời","Trả lời điện thoại.","<ruby>答<rt>こた</rt></ruby>える","<ruby>電話<rt>でんわ</rt></ruby>に<ruby>出<rt>で</rt></ruby>てください。","answer","Answer the phone.","Verb"],
  ["hỏi","Hỏi đường.","<ruby>聞<rt>き</rt></ruby>く","<ruby>道<rt>みち</rt></ruby>を<ruby>聞<rt>き</rt></ruby>く。","ask","Ask for directions.","Verb"],
  ["hứa","Tôi hứa.","<ruby>約束<rt>やくそく</rt></ruby>する","<ruby>約束<rt>やくそく</rt></ruby>します。","promise","I promise.","Verb"],
  ["tin","Tin tôi đi.","<ruby>信<rt>しん</rt></ruby>じる","<ruby>信<rt>しん</rt></ruby>じてください。","trust","Trust me.","Verb"],
  ["nghi ngờ","Tôi nghi ngờ.","<ruby>疑<rt>うたが</rt></ruby>う","<ruby>疑<rt>うたが</rt></ruby>っています。","doubt","I doubt it.","Verb"],
  ["thông cảm","Mong anh thông cảm.","ご<ruby>理解<rt>りかい</rt></ruby>ください","ご<ruby>理解<rt>りかい</rt></ruby>ください。","understand","Please understand.","Verb"],
  ["đồng ý","Tôi đồng ý.","<ruby>同意<rt>どうい</rt></ruby>する","<ruby>同意<rt>どうい</rt></ruby>します。","agree","I agree.","Verb"],
  ["phản đối","Tôi phản đối.","<ruby>反対<rt>はんたい</rt></ruby>する","<ruby>反対<rt>はんたい</rt></ruby>します。","oppose","I oppose.","Verb"],
  ["tham gia","Tôi muốn tham gia.","<ruby>参加<rt>さんか</rt></ruby>する","<ruby>参加<rt>さんか</rt></ruby>したいです。","join","I want to join.","Verb"],
  ["rút lui","Tôi xin rút lui.","<ruby>辞退<rt>じたい</rt></ruby>する","<ruby>辞退<rt>じたい</rt></ruby>します。","withdraw","I withdraw.","Verb"],
  ["tiếp tục","Hãy tiếp tục.","<ruby>続<rt>つづ</rt></ruby>ける","<ruby>続<rt>つづ</rt></ruby>けてください。","continue","Please continue.","Verb"],
  ["dừng","Dừng lại.","<ruby>止<rt>と</rt></ruby>まる","<ruby>止<rt>と</rt></ruby>まって。","stop","Stop.","Verb"],
  ["xong","Xong rồi.","<ruby>終<rt>お</rt></ruby>わった","<ruby>終<rt>お</rt></ruby>わりました。","done","Done.","Verb"],
  ["bắt","Bắt cá.","<ruby>捕<rt>と</rt></ruby>まえる","<ruby>魚<rt>さかな</rt></ruby>を<ruby>捕<rt>と</rt></ruby>まえる。","catch","Catch fish.","Verb"],
  ["thả","Thả con cá ra.","<ruby>放<rt>はな</rt></ruby>す","<ruby>魚<rt>さかな</rt></ruby>を<ruby>放<rt>はな</rt></ruby>す。","release","Release the fish.","Verb"],
  ["nhặt","Nhặt cái này lên.","<ruby>拾<rt>ひろ</rt></ruby>う","これを<ruby>拾<rt>ひろ</rt></ruby>って。","pick up","Pick this up.","Verb"],
  ["bỏ","Bỏ rác vào thùng.","<ruby>捨<rt>す</rt></ruby>てる","ゴミを<ruby>捨<rt>す</rt></ruby>ててください。","discard","Throw in the bin.","Verb"],
  ["mưa nhỏ","Trời mưa nhỏ.","<ruby>小雨<rt>こさめ</rt></ruby>","<ruby>小雨<rt>こさめ</rt></ruby>です。","light rain","Light rain.","Adjective"],
  ["mưa to","Mưa to lắm.","<ruby>大雨<rt>おおあめ</rt></ruby>","<ruby>大雨<rt>おおあめ</rt></ruby>です。","heavy rain","Heavy rain.","Adjective"],
  ["nắng to","Hôm nay nắng to.","<ruby>日差<rt>ひざ</rt></ruby>しが<ruby>強<rt>つよ</rt></ruby>い","<ruby>日差<rt>ひざ</rt></ruby>しが<ruby>強<rt>つよ</rt></ruby>いです。","strong sun","Strong sun today.","Adjective"],
  ["khói","Có nhiều khói.","<ruby>煙<rt>けむり</rt></ruby>","<ruby>煙<rt>けむり</rt></ruby>がたくさん。","smoke","Lots of smoke.","Noun"],
  ["bụi","Bụi nhiều quá.","ほこり","ほこりがすごい。","dust","Lots of dust.","Noun"],
  ["mùi","Có mùi gì lạ.","<ruby>匂<rt>にお</rt></ruby>い","<ruby>変<rt>へん</rt></ruby>な<ruby>匂<rt>にお</rt></ruby>い。","smell","Strange smell.","Noun"],
  ["thơm","Hoa thơm quá.","いい<ruby>香<rt>かお</rt></ruby>り","<ruby>花<rt>はな</rt></ruby>がいい<ruby>香<rt>かお</rt></ruby>り。","fragrant","Flowers smell good.","Adjective"],
  ["hôi","Mùi hôi quá.","<ruby>臭<rt>くさ</rt></ruby>い","<ruby>臭<rt>くさ</rt></ruby>いです。","smelly","Smelly.","Adjective"],
  ["tiếng","Tiếng còi xe.","<ruby>音<rt>おと</rt></ruby>","<ruby>車<rt>くるま</rt></ruby>のクラクションの<ruby>音<rt>おと</rt></ruby>。","sound","Car horn sound.","Noun"],
  ["giọng","Giọng anh hay.","<ruby>声<rt>こえ</rt></ruby>","いい<ruby>声<rt>こえ</rt></ruby>ですね。","voice","Nice voice.","Noun"],
  ["chữ","Chữ Hán khó.","<ruby>字<rt>じ</rt></ruby> / <ruby>文字<rt>もじ</rt></ruby>","<ruby>漢字<rt>かんじ</rt></ruby>は<ruby>難<rt>むずか</rt></ruby>しい。","character","Kanji is hard.","Noun"],
  ["số","Số điện thoại của anh?","<ruby>番号<rt>ばんごう</rt></ruby>","あなたの<ruby>電話番号<rt>でんわばんごう</rt></ruby>は?","number","Your phone number?","Noun"],
  ["bài","Bài này khó.","レッスン","このレッスンは<ruby>難<rt>むずか</rt></ruby>しい。","lesson","This lesson is hard.","Noun"],
  ["lỗi","Có lỗi rồi.","エラー","エラーが<ruby>出<rt>で</rt></ruby>ました。","error","There's an error.","Noun"],
  ["vấn đề","Có vấn đề gì?","<ruby>問題<rt>もんだい</rt></ruby>","<ruby>何<rt>なに</rt></ruby>か<ruby>問題<rt>もんだい</rt></ruby>?","problem","Any problem?","Noun"],
  ["giải pháp","Cần một giải pháp.","<ruby>解決策<rt>かいけつさく</rt></ruby>","<ruby>解決策<rt>かいけつさく</rt></ruby>が<ruby>必要<rt>ひつよう</rt></ruby>。","solution","Need a solution.","Noun"],
]

HTML = ROOT / "flashcard.html"
INDEX = ROOT / "index.html"
html = HTML.read_text(encoding="utf-8")
m = re.search(r'const D=(\[.*?\]);', html, re.DOTALL)
existing = json.loads(m.group(1))
existing_vn_lower = {c["vn"].lower() for c in existing}
existing_no_max = max(c["no"] for c in existing)

added, skipped = 0, 0
to_add = []
for vn, vn_ex, jp, jp_ex, en, en_ex, tag in NEW:
    if vn.lower() in existing_vn_lower:
        skipped += 1; continue
    existing_no_max += 1
    to_add.append({
        "no": existing_no_max, "cat": "Core Basic", "vn": vn,
        "vn_a": vn_ex, "vn_b": vn_ex, "jp": jp, "jp_a": jp_ex, "jp_b": jp_ex,
        "en": en, "en_a": en_ex, "en_b": en_ex, "tag": tag,
    })
    existing_vn_lower.add(vn.lower())
    added += 1

merged = existing + to_add
core_count = sum(1 for c in merged if c["cat"] == "Core Basic")
print(f"Added: {added}, Skipped: {skipped}, Core Basic now: {core_count}, Total: {len(merged)}")

(ROOT / "data" / "word_cards_v2.json").write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
data_line = "const D=" + json.dumps(merged, ensure_ascii=False) + ";"
new_html = re.sub(r'const D=\[.*?\];', lambda _: data_line, html, count=1, flags=re.DOTALL)
HTML.write_text(new_html, encoding="utf-8")
INDEX.write_text(new_html, encoding="utf-8")
