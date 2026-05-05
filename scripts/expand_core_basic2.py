#!/usr/bin/env python3
"""Add 141 more Core Basic cards to reach 500."""
import json, re
from pathlib import Path

ROOT = Path(__file__).parent.parent
HTML = ROOT / "flashcard.html"
INDEX = ROOT / "index.html"

NEW = [
  # ── More verbs (35) ─────────────────────────────────────────
  ["thuê","Tôi muốn thuê xe.","<ruby>借<rt>か</rt></ruby>りる","<ruby>車<rt>くるま</rt></ruby>を<ruby>借<rt>か</rt></ruby>りたいです。","rent","I want to rent a car.","Verb"],
  ["đặt","Tôi đã đặt phòng.","<ruby>予約<rt>よやく</rt></ruby>する","<ruby>部屋<rt>へや</rt></ruby>を<ruby>予約<rt>よやく</rt></ruby>しました。","book/reserve","I booked a room.","Verb"],
  ["huỷ","Huỷ đặt phòng.","キャンセルする","<ruby>予約<rt>よやく</rt></ruby>をキャンセルする。","cancel","Cancel the booking.","Verb"],
  ["đổi","Đổi tiền ở đâu?","<ruby>両替<rt>りょうがえ</rt></ruby>する","どこで<ruby>両替<rt>りょうがえ</rt></ruby>しますか?","exchange","Where to exchange?","Verb"],
  ["tăng","Giá tăng nhiều.","<ruby>上<rt>あ</rt></ruby>がる","<ruby>値段<rt>ねだん</rt></ruby>が<ruby>上<rt>あ</rt></ruby>がります。","increase","Prices are rising.","Verb"],
  ["giảm","Giảm cân.","<ruby>減<rt>へ</rt></ruby>る","<ruby>体重<rt>たいじゅう</rt></ruby>が<ruby>減<rt>へ</rt></ruby>る。","decrease","Lose weight.","Verb"],
  ["lên","Lên tầng hai.","<ruby>上<rt>あ</rt></ruby>がる","<ruby>二階<rt>にかい</rt></ruby>へ<ruby>上<rt>あ</rt></ruby>がる。","go up","Go up to the 2nd floor.","Verb"],
  ["xuống","Xuống xe ở đây.","<ruby>降<rt>お</rt></ruby>りる","ここで<ruby>降<rt>お</rt></ruby>ります。","get off","Get off here.","Verb"],
  ["vào","Mời vào nhà.","<ruby>入<rt>はい</rt></ruby>る","お<ruby>入<rt>はい</rt></ruby>りください。","enter","Please come in.","Verb"],
  ["ra","Tôi ra ngoài chút.","<ruby>出<rt>で</rt></ruby>る","<ruby>少<rt>すこ</rt></ruby>し<ruby>出<rt>で</rt></ruby>かけます。","go out","I'll go out for a bit.","Verb"],
  ["quay lại","Tôi sẽ quay lại.","<ruby>戻<rt>もど</rt></ruby>る","<ruby>戻<rt>もど</rt></ruby>ります。","come back","I'll come back.","Verb"],
  ["dẫn","Dẫn tôi đi.","<ruby>案内<rt>あんない</rt></ruby>する","<ruby>案内<rt>あんない</rt></ruby>してください。","lead/guide","Show me the way.","Verb"],
  ["mời","Mời anh dùng cơm.","<ruby>招待<rt>しょうたい</rt></ruby>する","<ruby>食事<rt>しょくじ</rt></ruby>にお<ruby>招<rt>まね</rt></ruby>きします。","invite","Please join the meal.","Verb"],
  ["chia","Chia đều cho mọi người.","<ruby>分<rt>わ</rt></ruby>ける","みんなで<ruby>分<rt>わ</rt></ruby>けます。","divide","Divide among everyone.","Verb"],
  ["đếm","Đếm tiền giúp tôi.","<ruby>数<rt>かぞ</rt></ruby>える","お<ruby>金<rt>かね</rt></ruby>を<ruby>数<rt>かぞ</rt></ruby>えてください。","count","Count the money please.","Verb"],
  ["đo","Đo nhiệt độ.","<ruby>測<rt>はか</rt></ruby>る","<ruby>体温<rt>たいおん</rt></ruby>を<ruby>測<rt>はか</rt></ruby>ります。","measure","Measure temperature.","Verb"],
  ["cân","Cân nặng bao nhiêu?","<ruby>体重<rt>たいじゅう</rt></ruby>","<ruby>体重<rt>たいじゅう</rt></ruby>はどのくらい?","weigh","How much do you weigh?","Verb"],
  ["thuộc","Tôi thuộc bài.","<ruby>暗記<rt>あんき</rt></ruby>する","<ruby>暗記<rt>あんき</rt></ruby>しました。","memorize","I memorized.","Verb"],
  ["đoán","Anh đoán xem.","<ruby>当<rt>あ</rt></ruby>てる","<ruby>当<rt>あ</rt></ruby>ててみて。","guess","Take a guess.","Verb"],
  ["chọn","Chọn món gì?","<ruby>選<rt>えら</rt></ruby>ぶ","<ruby>何<rt>なに</rt></ruby>を<ruby>選<rt>えら</rt></ruby>びますか?","choose","What do you choose?","Verb"],
  ["nghỉ","Tôi muốn nghỉ ngơi.","<ruby>休<rt>やす</rt></ruby>む","<ruby>休<rt>やす</rt></ruby>みたいです。","rest","I want to rest.","Verb"],
  ["khóa","Khóa cửa lại.","<ruby>鍵<rt>かぎ</rt></ruby>を<ruby>掛<rt>か</rt></ruby>ける","ドアに<ruby>鍵<rt>かぎ</rt></ruby>を<ruby>掛<rt>か</rt></ruby>けてください。","lock","Lock the door.","Verb"],
  ["cắt","Cắt tóc đi.","<ruby>切<rt>き</rt></ruby>る","<ruby>髪<rt>かみ</rt></ruby>を<ruby>切<rt>き</rt></ruby>ってください。","cut","Get a haircut.","Verb"],
  ["dán","Dán nhãn vào.","<ruby>貼<rt>は</rt></ruby>る","ラベルを<ruby>貼<rt>は</rt></ruby>ってください。","stick/paste","Paste the label.","Verb"],
  ["lau","Lau bàn sạch.","<ruby>拭<rt>ふ</rt></ruby>く","テーブルを<ruby>拭<rt>ふ</rt></ruby>いてください。","wipe","Wipe the table.","Verb"],
  ["quét","Quét nhà.","<ruby>掃<rt>は</rt></ruby>く","<ruby>家<rt>いえ</rt></ruby>を<ruby>掃<rt>は</rt></ruby>く。","sweep","Sweep the house.","Verb"],
  ["tưới","Tưới cây mỗi sáng.","<ruby>水<rt>みず</rt></ruby>をやる","<ruby>毎朝<rt>まいあさ</rt></ruby><ruby>水<rt>みず</rt></ruby>をやります。","water (plants)","Water plants every morning.","Verb"],
  ["chăm sóc","Chăm sóc em bé.","<ruby>世話<rt>せわ</rt></ruby>する","<ruby>赤<rt>あか</rt></ruby>ちゃんの<ruby>世話<rt>せわ</rt></ruby>をする。","care for","Take care of baby.","Verb"],
  ["bế","Bế em bé giúp tôi.","<ruby>抱<rt>だ</rt></ruby>っこする","<ruby>赤<rt>あか</rt></ruby>ちゃんを<ruby>抱<rt>だ</rt></ruby>っこしてください。","hold (baby)","Hold the baby for me.","Verb"],
  ["ôm","Ôm tôi nhé.","<ruby>抱<rt>だ</rt></ruby>きしめる","<ruby>抱<rt>だ</rt></ruby>きしめて。","hug","Hug me.","Verb"],
  ["hôn","Hôn tạm biệt.","キス / <ruby>口<rt>くち</rt></ruby>づけ","お<ruby>別<rt>わか</rt></ruby>れのキス。","kiss","Goodbye kiss.","Verb"],
  ["bắt tay","Bắt tay làm quen.","<ruby>握手<rt>あくしゅ</rt></ruby>する","<ruby>握手<rt>あくしゅ</rt></ruby>しましょう。","shake hands","Let's shake hands.","Verb"],
  ["khen","Sếp khen tôi.","ほめる","<ruby>上司<rt>じょうし</rt></ruby>がほめてくれました。","praise","Boss praised me.","Verb"],
  ["chê","Đừng chê tôi.","けなす","けなさないで。","criticize","Don't criticize me.","Verb"],
  ["kể","Kể chuyện cho tôi nghe.","<ruby>話<rt>はな</rt></ruby>す","お<ruby>話<rt>はなし</rt></ruby>を<ruby>聞<rt>き</rt></ruby>かせてください。","tell","Tell me a story.","Verb"],

  # ── More adjectives (25) ────────────────────────────────────
  ["vui","Tôi rất vui.","<ruby>楽<rt>たの</rt></ruby>しい","とても<ruby>楽<rt>たの</rt></ruby>しいです。","fun","I'm having fun.","Adjective"],
  ["cô đơn","Cảm thấy cô đơn.","<ruby>寂<rt>さび</rt></ruby>しい","<ruby>寂<rt>さび</rt></ruby>しいです。","lonely","I feel lonely.","Adjective"],
  ["bình tĩnh","Hãy bình tĩnh.","<ruby>落<rt>お</rt></ruby>ち<ruby>着<rt>つ</rt></ruby>いて","<ruby>落<rt>お</rt></ruby>ち<ruby>着<rt>つ</rt></ruby>いてください。","calm","Stay calm.","Adjective"],
  ["lo lắng","Đừng lo lắng.","<ruby>心配<rt>しんぱい</rt></ruby>","<ruby>心配<rt>しんぱい</rt></ruby>しないで。","worried","Don't worry.","Adjective"],
  ["tự tin","Anh tự tin lắm.","<ruby>自信<rt>じしん</rt></ruby>","<ruby>自信<rt>じしん</rt></ruby>がありますね。","confident","You're confident.","Adjective"],
  ["xấu hổ","Tôi xấu hổ quá.","<ruby>恥<rt>は</rt></ruby>ずかしい","<ruby>恥<rt>は</rt></ruby>ずかしいです。","embarrassed","I'm embarrassed.","Adjective"],
  ["tốt bụng","Anh ấy tốt bụng.","<ruby>優<rt>やさ</rt></ruby>しい","<ruby>彼<rt>かれ</rt></ruby>は<ruby>優<rt>やさ</rt></ruby>しいです。","kind","He's kind.","Adjective"],
  ["thật thà","Em thật thà.","<ruby>正直<rt>しょうじき</rt></ruby>","あなたは<ruby>正直<rt>しょうじき</rt></ruby>です。","honest","You're honest.","Adjective"],
  ["lười","Đừng lười.","<ruby>怠<rt>なま</rt></ruby>け<ruby>者<rt>もの</rt></ruby>","<ruby>怠<rt>なま</rt></ruby>けないで。","lazy","Don't be lazy.","Adjective"],
  ["chăm chỉ","Sinh viên chăm chỉ.","<ruby>勤勉<rt>きんべん</rt></ruby>","<ruby>勤勉<rt>きんべん</rt></ruby>な<ruby>学生<rt>がくせい</rt></ruby>です。","diligent","Diligent student.","Adjective"],
  ["khôn","Em bé khôn.","<ruby>賢<rt>かしこ</rt></ruby>い","<ruby>賢<rt>かしこ</rt></ruby>い<ruby>子<rt>こ</rt></ruby>です。","clever","Clever child.","Adjective"],
  ["ngu","Đừng làm chuyện ngu.","<ruby>愚<rt>おろ</rt></ruby>か","<ruby>愚<rt>おろ</rt></ruby>かなことをしないで。","stupid","Don't do stupid things.","Adjective"],
  ["lịch sự","Anh rất lịch sự.","<ruby>礼儀<rt>れいぎ</rt></ruby><ruby>正<rt>ただ</rt></ruby>しい","とても<ruby>礼儀<rt>れいぎ</rt></ruby><ruby>正<rt>ただ</rt></ruby>しいです。","polite","You're very polite.","Adjective"],
  ["thô lỗ","Đừng thô lỗ.","<ruby>失礼<rt>しつれい</rt></ruby>","<ruby>失礼<rt>しつれい</rt></ruby>しないで。","rude","Don't be rude.","Adjective"],
  ["đói","Tôi đói rồi.","お<ruby>腹<rt>なか</rt></ruby>がすいた","お<ruby>腹<rt>なか</rt></ruby>がすきました。","hungry","I'm hungry.","Adjective"],
  ["no","Tôi no rồi.","お<ruby>腹<rt>なか</rt></ruby>いっぱい","お<ruby>腹<rt>なか</rt></ruby>いっぱいです。","full","I'm full.","Adjective"],
  ["khát","Tôi khát nước.","のどが<ruby>渇<rt>かわ</rt></ruby>いた","のどが<ruby>渇<rt>かわ</rt></ruby>きました。","thirsty","I'm thirsty.","Adjective"],
  ["mệt","Tôi mệt quá.","<ruby>疲<rt>つか</rt></ruby>れた","<ruby>疲<rt>つか</rt></ruby>れました。","tired","I'm tired.","Adjective"],
  ["buồn ngủ","Tôi buồn ngủ.","<ruby>眠<rt>ねむ</rt></ruby>い","<ruby>眠<rt>ねむ</rt></ruby>いです。","sleepy","I'm sleepy.","Adjective"],
  ["thoáng","Phòng thoáng mát.","<ruby>風通<rt>かぜとお</rt></ruby>しの<ruby>良<rt>よ</rt></ruby>い","<ruby>風通<rt>かぜとお</rt></ruby>しの<ruby>良<rt>よ</rt></ruby>い<ruby>部屋<rt>へや</rt></ruby>。","airy","Airy room.","Adjective"],
  ["chật","Phòng chật quá.","<ruby>狭<rt>せま</rt></ruby>い","<ruby>部屋<rt>へや</rt></ruby>が<ruby>狭<rt>せま</rt></ruby>すぎます。","cramped","Room is too cramped.","Adjective"],
  ["nhẹ","Hành lý nhẹ.","<ruby>軽<rt>かる</rt></ruby>い","<ruby>荷物<rt>にもつ</rt></ruby>が<ruby>軽<rt>かる</rt></ruby>いです。","light (weight)","Light luggage.","Adjective"],
  ["miễn phí","Wifi miễn phí.","<ruby>無料<rt>むりょう</rt></ruby>","Wi-Fiは<ruby>無料<rt>むりょう</rt></ruby>です。","free","Wifi is free.","Adjective"],
  ["mất phí","Dịch vụ mất phí.","<ruby>有料<rt>ゆうりょう</rt></ruby>","サービスは<ruby>有料<rt>ゆうりょう</rt></ruby>です。","paid","Paid service.","Adjective"],
  ["tươi","Cá tươi lắm.","<ruby>新鮮<rt>しんせん</rt></ruby>","<ruby>魚<rt>さかな</rt></ruby>はとても<ruby>新鮮<rt>しんせん</rt></ruby>です。","fresh","Very fresh fish.","Adjective"],

  # ── Tools/Things (20) ───────────────────────────────────────
  ["sách","Tôi đọc sách.","<ruby>本<rt>ほん</rt></ruby>","<ruby>本<rt>ほん</rt></ruby>を<ruby>読<rt>よ</rt></ruby>みます。","book","I read books.","Noun"],
  ["bút","Cho mượn bút.","ペン","ペンを<ruby>貸<rt>か</rt></ruby>してください。","pen","Lend me a pen.","Noun"],
  ["giấy","Tờ giấy trắng.","<ruby>紙<rt>かみ</rt></ruby>","<ruby>白<rt>しろ</rt></ruby>い<ruby>紙<rt>かみ</rt></ruby>。","paper","White paper.","Noun"],
  ["bàn","Bàn gỗ.","<ruby>机<rt>つくえ</rt></ruby>","<ruby>木<rt>き</rt></ruby>の<ruby>机<rt>つくえ</rt></ruby>。","desk","Wooden desk.","Noun"],
  ["ghế","Ngồi ghế đi.","<ruby>椅子<rt>いす</rt></ruby>","<ruby>椅子<rt>いす</rt></ruby>に<ruby>座<rt>すわ</rt></ruby>って。","chair","Sit on the chair.","Noun"],
  ["máy tính","Máy tính bị hỏng.","パソコン","パソコンが<ruby>壊<rt>こわ</rt></ruby>れました。","computer","Computer is broken.","Noun"],
  ["điện thoại","Điện thoại đời mới.","<ruby>携帯<rt>けいたい</rt></ruby><ruby>電話<rt>でんわ</rt></ruby>","<ruby>新<rt>あたら</rt></ruby>しい<ruby>携帯<rt>けいたい</rt></ruby>。","phone","New phone.","Noun"],
  ["wifi","Có wifi không?","Wi-Fi","Wi-Fiはありますか?","wifi","Is there wifi?","Noun"],
  ["mật khẩu","Mật khẩu là gì?","パスワード","パスワードは<ruby>何<rt>なん</rt></ruby>ですか?","password","What's the password?","Noun"],
  ["pin","Pin sắp hết.","<ruby>電池<rt>でんち</rt></ruby>","<ruby>電池<rt>でんち</rt></ruby>がなくなります。","battery","Battery is dying.","Noun"],
  ["sạc","Cho mượn sạc.","<ruby>充電器<rt>じゅうでんき</rt></ruby>","<ruby>充電器<rt>じゅうでんき</rt></ruby>を<ruby>貸<rt>か</rt></ruby>してください。","charger","Lend me a charger.","Noun"],
  ["phim","Phim hay không?","<ruby>映画<rt>えいが</rt></ruby>","<ruby>面白<rt>おもしろ</rt></ruby>い<ruby>映画<rt>えいが</rt></ruby>?","movie","Is the movie good?","Noun"],
  ["nhạc","Tôi nghe nhạc Việt.","<ruby>音楽<rt>おんがく</rt></ruby>","ベトナムの<ruby>音楽<rt>おんがく</rt></ruby>を<ruby>聞<rt>き</rt></ruby>く。","music","I listen to Viet music.","Noun"],
  ["bài hát","Bài hát hay quá.","<ruby>歌<rt>うた</rt></ruby>","いい<ruby>歌<rt>うた</rt></ruby>です。","song","Great song.","Noun"],
  ["trò chơi","Tôi thích trò chơi.","ゲーム","ゲームが<ruby>好<rt>す</rt></ruby>きです。","game","I like games.","Noun"],
  ["ảnh","Ảnh đẹp quá.","<ruby>写真<rt>しゃしん</rt></ruby>","きれいな<ruby>写真<rt>しゃしん</rt></ruby>です。","photo","Beautiful photo.","Noun"],
  ["video","Quay video lại.","<ruby>動画<rt>どうが</rt></ruby>","<ruby>動画<rt>どうが</rt></ruby>を<ruby>撮<rt>と</rt></ruby>る。","video","Record a video.","Noun"],
  ["tin nhắn","Gửi tin nhắn cho tôi.","メッセージ","メッセージを<ruby>送<rt>おく</rt></ruby>ってください。","message","Send me a message.","Noun"],
  ["email","Tôi nhận email rồi.","メール","メールを<ruby>受<rt>う</rt></ruby>け<ruby>取<rt>と</rt></ruby>りました。","email","I got the email.","Noun"],
  ["mạng","Mạng yếu quá.","インターネット","インターネットが<ruby>遅<rt>おそ</rt></ruby>いです。","internet","Internet is slow.","Noun"],

  # ── Useful expressions (20) ─────────────────────────────────
  ["có lẽ","Có lẽ trời sẽ mưa.","たぶん","たぶん<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>ります。","maybe","It might rain.","Adverb"],
  ["chắc chắn","Chắc chắn đúng.","<ruby>確<rt>たし</rt></ruby>か","<ruby>確<rt>たし</rt></ruby>かに<ruby>正<rt>ただ</rt></ruby>しい。","sure","Definitely right.","Adverb"],
  ["có thể","Tôi có thể giúp.","できる","<ruby>手伝<rt>てつだ</rt></ruby>えます。","can","I can help.","Adverb"],
  ["không thể","Không thể được.","できない","できません。","cannot","Cannot be done.","Adverb"],
  ["nên","Anh nên đi sớm.","~した<ruby>方<rt>ほう</rt></ruby>がいい","<ruby>早<rt>はや</rt></ruby>く<ruby>行<rt>い</rt></ruby>った<ruby>方<rt>ほう</rt></ruby>がいい。","should","You should go early.","Adverb"],
  ["không nên","Không nên hút thuốc.","~しない<ruby>方<rt>ほう</rt></ruby>がいい","タバコを<ruby>吸<rt>す</rt></ruby>わない<ruby>方<rt>ほう</rt></ruby>がいい。","shouldn't","You shouldn't smoke.","Adverb"],
  ["phải","Phải làm bây giờ.","しなければ","<ruby>今<rt>いま</rt></ruby>しなければなりません。","must","Must do now.","Adverb"],
  ["thường","Tôi thường đi sớm.","よく","よく<ruby>早<rt>はや</rt></ruby>く<ruby>行<rt>い</rt></ruby>きます。","often","I often go early.","Adverb"],
  ["đôi khi","Đôi khi tôi quên.","<ruby>時々<rt>ときどき</rt></ruby>","<ruby>時々<rt>ときどき</rt></ruby><ruby>忘<rt>わす</rt></ruby>れます。","sometimes","Sometimes I forget.","Adverb"],
  ["hiếm khi","Hiếm khi tôi đi muộn.","めったに~ない","めったに<ruby>遅刻<rt>ちこく</rt></ruby>しません。","rarely","I rarely arrive late.","Adverb"],
  ["mới đây","Mới đây tôi gặp anh ấy.","<ruby>最近<rt>さいきん</rt></ruby>","<ruby>最近<rt>さいきん</rt></ruby><ruby>彼<rt>かれ</rt></ruby>に<ruby>会<rt>あ</rt></ruby>いました。","recently","Recently met him.","Adverb"],
  ["lần đầu","Lần đầu đến đây.","<ruby>初<rt>はじ</rt></ruby>めて","<ruby>初<rt>はじ</rt></ruby>めて<ruby>来<rt>き</rt></ruby>ました。","first time","First time here.","Adverb"],
  ["cuối cùng","Cuối cùng cũng xong.","ついに","ついに<ruby>終<rt>お</rt></ruby>わりました。","finally","Finally done.","Adverb"],
  ["sau đó","Sau đó chúng tôi về nhà.","その<ruby>後<rt>あと</rt></ruby>","その<ruby>後<rt>あと</rt></ruby><ruby>家<rt>いえ</rt></ruby>に<ruby>帰<rt>かえ</rt></ruby>りました。","after that","After that we went home.","Adverb"],
  ["trước đó","Trước đó tôi đã ăn.","その<ruby>前<rt>まえ</rt></ruby>","その<ruby>前<rt>まえ</rt></ruby>に<ruby>食<rt>た</rt></ruby>べました。","before that","Before that I ate.","Adverb"],
  ["xin chào ạ","Xin chào ạ.","こんにちは","こんにちは。","hello (polite)","Hello (polite).","Greeting"],
  ["dạ","Dạ vâng.","はい","はい。","yes (polite)","Yes (polite).","Response"],
  ["dạ không","Dạ không.","いいえ","いいえ。","no (polite)","No (polite).","Response"],
  ["được rồi","Được rồi nhé.","いいよ / OK","いいですよ。","okay","Okay.","Response"],
  ["thôi nào","Thôi nào, đi đi.","さあ、<ruby>行<rt>い</rt></ruby>こう","さあ、<ruby>行<rt>い</rt></ruby>きましょう。","come on","Come on, let's go.","Greeting"],

  # ── Direction/Position (15) ─────────────────────────────────
  ["bên trái","Rẽ bên trái.","<ruby>左<rt>ひだり</rt></ruby>","<ruby>左<rt>ひだり</rt></ruby>に<ruby>曲<rt>ま</rt></ruby>がる。","left","Turn left.","Adverb"],
  ["bên phải","Rẽ bên phải.","<ruby>右<rt>みぎ</rt></ruby>","<ruby>右<rt>みぎ</rt></ruby>に<ruby>曲<rt>ま</rt></ruby>がる。","right","Turn right.","Adverb"],
  ["thẳng","Đi thẳng.","まっすぐ","まっすぐ<ruby>行<rt>い</rt></ruby>く。","straight","Go straight.","Adverb"],
  ["phía trước","Phía trước có quán.","<ruby>前<rt>まえ</rt></ruby>","<ruby>前<rt>まえ</rt></ruby>に<ruby>店<rt>みせ</rt></ruby>があります。","ahead","A shop ahead.","Adverb"],
  ["phía sau","Phía sau nhà.","<ruby>後<rt>うし</rt></ruby>ろ","<ruby>家<rt>いえ</rt></ruby>の<ruby>後<rt>うし</rt></ruby>ろ。","behind","Behind the house.","Adverb"],
  ["bên trên","Để bên trên bàn.","<ruby>上<rt>うえ</rt></ruby>","<ruby>机<rt>つくえ</rt></ruby>の<ruby>上<rt>うえ</rt></ruby>に<ruby>置<rt>お</rt></ruby>く。","on top","Place on the desk.","Adverb"],
  ["bên dưới","Bên dưới ghế.","<ruby>下<rt>した</rt></ruby>","<ruby>椅子<rt>いす</rt></ruby>の<ruby>下<rt>した</rt></ruby>。","below","Under the chair.","Adverb"],
  ["bên trong","Bên trong phòng.","<ruby>中<rt>なか</rt></ruby>","<ruby>部屋<rt>へや</rt></ruby>の<ruby>中<rt>なか</rt></ruby>。","inside","Inside the room.","Adverb"],
  ["bên ngoài","Bên ngoài cửa.","<ruby>外<rt>そと</rt></ruby>","ドアの<ruby>外<rt>そと</rt></ruby>。","outside","Outside the door.","Adverb"],
  ["giữa","Đứng giữa hai người.","<ruby>間<rt>あいだ</rt></ruby>","<ruby>二人<rt>ふたり</rt></ruby>の<ruby>間<rt>あいだ</rt></ruby>に<ruby>立<rt>た</rt></ruby>つ。","between","Stand between two.","Adverb"],
  ["đối diện","Đối diện ngân hàng.","<ruby>向<rt>む</rt></ruby>かい","<ruby>銀行<rt>ぎんこう</rt></ruby>の<ruby>向<rt>む</rt></ruby>かい。","opposite","Across from bank.","Adverb"],
  ["bên cạnh","Bên cạnh trường.","<ruby>横<rt>よこ</rt></ruby>","<ruby>学校<rt>がっこう</rt></ruby>の<ruby>横<rt>よこ</rt></ruby>。","next to","Next to school.","Adverb"],
  ["xa","Nhà ga xa quá.","<ruby>遠<rt>とお</rt></ruby>い","<ruby>駅<rt>えき</rt></ruby>は<ruby>遠<rt>とお</rt></ruby>すぎます。","far","Station is too far.","Adjective"],
  ["gần","Gần nhà tôi.","<ruby>近<rt>ちか</rt></ruby>い","<ruby>家<rt>いえ</rt></ruby>に<ruby>近<rt>ちか</rt></ruby>いです。","near","Near my home.","Adjective"],
  ["khắp nơi","Khắp nơi đều có.","あちこち","あちこちにあります。","everywhere","Everywhere.","Adverb"],

  # ── Time more (15) ──────────────────────────────────────────
  ["buổi sáng","Buổi sáng yên tĩnh.","<ruby>朝<rt>あさ</rt></ruby>","<ruby>朝<rt>あさ</rt></ruby>は<ruby>静<rt>しず</rt></ruby>かです。","morning","Quiet morning.","Time"],
  ["buổi chiều","Buổi chiều nóng.","<ruby>午後<rt>ごご</rt></ruby>","<ruby>午後<rt>ごご</rt></ruby>は<ruby>暑<rt>あつ</rt></ruby>いです。","afternoon","Hot afternoon.","Time"],
  ["nửa đêm","Nửa đêm tỉnh giấc.","<ruby>真夜中<rt>まよなか</rt></ruby>","<ruby>真夜中<rt>まよなか</rt></ruby>に<ruby>目<rt>め</rt></ruby>が<ruby>覚<rt>さ</rt></ruby>めた。","midnight","Woke up at midnight.","Time"],
  ["đầu năm","Đầu năm đi du lịch.","<ruby>年初<rt>ねんしょ</rt></ruby>","<ruby>年初<rt>ねんしょ</rt></ruby>に<ruby>旅行<rt>りょこう</rt></ruby>します。","beginning of year","Travel at year start.","Time"],
  ["cuối năm","Cuối năm bận lắm.","<ruby>年末<rt>ねんまつ</rt></ruby>","<ruby>年末<rt>ねんまつ</rt></ruby>は<ruby>忙<rt>いそが</rt></ruby>しいです。","end of year","Year end is busy.","Time"],
  ["đầu tuần","Đầu tuần nhiều việc.","<ruby>週<rt>しゅう</rt></ruby>の<ruby>初<rt>はじ</rt></ruby>め","<ruby>週<rt>しゅう</rt></ruby>の<ruby>初<rt>はじ</rt></ruby>めは<ruby>忙<rt>いそが</rt></ruby>しい。","beginning of week","Busy start of week.","Time"],
  ["cuối tuần","Cuối tuần đi chơi.","<ruby>週末<rt>しゅうまつ</rt></ruby>","<ruby>週末<rt>しゅうまつ</rt></ruby>に<ruby>遊<rt>あそ</rt></ruby>びに<ruby>行<rt>い</rt></ruby>く。","weekend","Going out on weekend.","Time"],
  ["tháng trước","Tháng trước tôi nghỉ.","<ruby>先月<rt>せんげつ</rt></ruby>","<ruby>先月<rt>せんげつ</rt></ruby><ruby>休<rt>やす</rt></ruby>みました。","last month","I rested last month.","Time"],
  ["tháng sau","Tháng sau gặp lại.","<ruby>来月<rt>らいげつ</rt></ruby>","<ruby>来月<rt>らいげつ</rt></ruby>また<ruby>会<rt>あ</rt></ruby>いましょう。","next month","See you next month.","Time"],
  ["dạo này","Dạo này khoẻ không?","<ruby>最近<rt>さいきん</rt></ruby>","<ruby>最近<rt>さいきん</rt></ruby><ruby>元気<rt>げんき</rt></ruby>?","these days","How are you these days?","Time"],
  ["lúc nào","Lúc nào cũng được.","いつでも","いつでもいいですよ。","whenever","Anytime is fine.","Time"],
  ["mãi mãi","Mãi mãi yêu em.","<ruby>永遠<rt>えいえん</rt></ruby>に","<ruby>永遠<rt>えいえん</rt></ruby>に<ruby>愛<rt>あい</rt></ruby>している。","forever","Love you forever.","Time"],
  ["tức thì","Cần ngay tức thì.","すぐに","すぐに<ruby>必要<rt>ひつよう</rt></ruby>です。","immediately","Need immediately.","Time"],
  ["sắp","Sắp đến giờ rồi.","もうすぐ","もうすぐ<ruby>時間<rt>じかん</rt></ruby>です。","about to","Almost time.","Time"],
  ["vừa mới","Tôi vừa mới ăn xong.","~したばかり","<ruby>食<rt>た</rt></ruby>べたばかりです。","just now","I just ate.","Time"],

  # ── Misc (11) ──────────────────────────────────────────────
  ["chuyện gì","Chuyện gì vậy?","<ruby>何<rt>なに</rt></ruby>のこと","<ruby>何<rt>なに</rt></ruby>のことですか?","what's up","What's going on?","Question"],
  ["thế thôi","Thế thôi à.","それだけ","それだけ?","that's all","That's all?","Response"],
  ["cũng vậy","Tôi cũng vậy.","<ruby>私<rt>わたし</rt></ruby>も","<ruby>私<rt>わたし</rt></ruby>もそうです。","me too","Me too.","Response"],
  ["rồi sao","Rồi sao nữa?","それで?","それでどうしたの?","then what","Then what?","Question"],
  ["đúng rồi","Đúng rồi đó.","そうです","そうです。","that's right","That's right.","Response"],
  ["sai rồi","Sai rồi.","<ruby>間違<rt>まちが</rt></ruby>えた","<ruby>間違<rt>まちが</rt></ruby>えました。","wrong","Wrong.","Response"],
  ["khoảng","Khoảng 5 giờ.","<ruby>約<rt>やく</rt></ruby>","<ruby>約<rt>やく</rt></ruby>5<ruby>時<rt>じ</rt></ruby>。","about","About 5 o'clock.","Adverb"],
  ["chính xác","Chính xác lắm.","<ruby>正確<rt>せいかく</rt></ruby>","<ruby>正確<rt>せいかく</rt></ruby>です。","exactly","Exactly.","Adverb"],
  ["khoảng cách","Khoảng cách xa.","<ruby>距離<rt>きょり</rt></ruby>","<ruby>距離<rt>きょり</rt></ruby>が<ruby>遠<rt>とお</rt></ruby>い。","distance","Far distance.","Noun"],
  ["chiều cao","Anh chiều cao bao nhiêu?","<ruby>身長<rt>しんちょう</rt></ruby>","<ruby>身長<rt>しんちょう</rt></ruby>は?","height","How tall are you?","Noun"],
  ["loại","Có nhiều loại.","<ruby>種類<rt>しゅるい</rt></ruby>","いろいろな<ruby>種類<rt>しゅるい</rt></ruby>があります。","kind/type","Many types.","Noun"],
]

html = HTML.read_text(encoding="utf-8")
m = re.search(r'const D=(\[.*?\]);', html, re.DOTALL)
existing = json.loads(m.group(1))
existing_vn_lower = {c["vn"].lower() for c in existing}
existing_no_max = max(c["no"] for c in existing)

added, skipped = 0, 0
to_add = []
for vn, vn_ex, jp, jp_ex, en, en_ex, tag in NEW:
    if vn.lower() in existing_vn_lower:
        skipped += 1
        continue
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
print(f"Added: {added}, Skipped: {skipped}, Core Basic now: {core_count}")
Path("data/word_cards_v2.json").write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")

data_line = "const D=" + json.dumps(merged, ensure_ascii=False) + ";"
new_html = re.sub(r'const D=\[.*?\];', lambda _: data_line, html, count=1, flags=re.DOTALL)
HTML.write_text(new_html, encoding="utf-8")
INDEX.write_text(new_html, encoding="utf-8")
print(f"Total cards now: {len(merged)}")
