#!/usr/bin/env python3
"""Add 242 new Core Basic cards to flashcard.html (target 500 total)."""
import json, re
from pathlib import Path

ROOT = Path(__file__).parent.parent
HTML = ROOT / "flashcard.html"
INDEX = ROOT / "index.html"

# 242 new entries. Schema: vn, vn_ex, jp (with ruby), jp_ex, en, en_ex, tag
NEW = [
  # ── Verbs (50) ───────────────────────────────────────────────
  ["dậy","Anh dậy lúc mấy giờ?","<ruby>起<rt>お</rt></ruby>きる","<ruby>何時<rt>なんじ</rt></ruby>に<ruby>起<rt>お</rt></ruby>きますか?","wake up","What time do you wake up?","Verb"],
  ["ngủ","Tôi ngủ tám tiếng.","<ruby>寝<rt>ね</rt></ruby>る","<ruby>八時間<rt>はちじかん</rt></ruby><ruby>寝<rt>ね</rt></ruby>ます。","sleep","I sleep eight hours.","Verb"],
  ["tắm","Tôi tắm buổi sáng.","シャワーを<ruby>浴<rt>あ</rt></ruby>びる","<ruby>朝<rt>あさ</rt></ruby>シャワーを<ruby>浴<rt>あ</rt></ruby>びます。","take a shower","I shower in the morning.","Verb"],
  ["rửa","Rửa tay trước khi ăn.","<ruby>洗<rt>あら</rt></ruby>う","<ruby>食<rt>た</rt></ruby>べる<ruby>前<rt>まえ</rt></ruby>に<ruby>手<rt>て</rt></ruby>を<ruby>洗<rt>あら</rt></ruby>います。","wash","Wash your hands before eating.","Verb"],
  ["nấu","Mẹ nấu cơm tối.","<ruby>作<rt>つく</rt></ruby>る","<ruby>母<rt>はは</rt></ruby>が<ruby>夕食<rt>ゆうしょく</rt></ruby>を<ruby>作<rt>つく</rt></ruby>ります。","cook","Mom cooks dinner.","Verb"],
  ["chờ","Xin chờ một chút.","<ruby>待<rt>ま</rt></ruby>つ","<ruby>少<rt>すこ</rt></ruby>し<ruby>待<rt>ま</rt></ruby>ってください。","wait","Please wait a moment.","Verb"],
  ["nhớ","Tôi nhớ bạn.","<ruby>覚<rt>おぼ</rt></ruby>える / <ruby>恋<rt>こい</rt></ruby>しい","あなたが<ruby>恋<rt>こい</rt></ruby>しいです。","miss/remember","I miss you.","Verb"],
  ["quên","Tôi quên rồi.","<ruby>忘<rt>わす</rt></ruby>れる","<ruby>忘<rt>わす</rt></ruby>れました。","forget","I forgot.","Verb"],
  ["nghĩ","Tôi nghĩ là đúng.","<ruby>思<rt>おも</rt></ruby>う","<ruby>正<rt>ただ</rt></ruby>しいと<ruby>思<rt>おも</rt></ruby>います。","think","I think it's right.","Verb"],
  ["yêu","Anh yêu em.","<ruby>愛<rt>あい</rt></ruby>している","<ruby>愛<rt>あい</rt></ruby>しています。","love","I love you.","Verb"],
  ["thích","Tôi thích cà phê.","<ruby>好<rt>す</rt></ruby>き","コーヒーが<ruby>好<rt>す</rt></ruby>きです。","like","I like coffee.","Verb"],
  ["ghét","Tôi ghét trễ giờ.","<ruby>嫌<rt>きら</rt></ruby>い","<ruby>遅刻<rt>ちこく</rt></ruby>が<ruby>嫌<rt>きら</rt></ruby>いです。","hate","I hate being late.","Verb"],
  ["sợ","Tôi sợ chó.","<ruby>怖<rt>こわ</rt></ruby>い","<ruby>犬<rt>いぬ</rt></ruby>が<ruby>怖<rt>こわ</rt></ruby>いです。","afraid","I'm afraid of dogs.","Verb"],
  ["cười","Em bé cười rất dễ thương.","<ruby>笑<rt>わら</rt></ruby>う","<ruby>赤<rt>あか</rt></ruby>ちゃんが<ruby>可愛<rt>かわい</rt></ruby>く<ruby>笑<rt>わら</rt></ruby>います。","laugh/smile","The baby smiles cutely.","Verb"],
  ["khóc","Em bé đang khóc.","<ruby>泣<rt>な</rt></ruby>く","<ruby>赤<rt>あか</rt></ruby>ちゃんが<ruby>泣<rt>な</rt></ruby>いています。","cry","The baby is crying.","Verb"],
  ["hát","Tôi thích hát karaoke.","<ruby>歌<rt>うた</rt></ruby>う","カラオケで<ruby>歌<rt>うた</rt></ruby>うのが<ruby>好<rt>す</rt></ruby>きです。","sing","I like singing karaoke.","Verb"],
  ["nhảy","Cô ấy nhảy đẹp.","<ruby>踊<rt>おど</rt></ruby>る","<ruby>彼女<rt>かのじょ</rt></ruby>は<ruby>上手<rt>じょうず</rt></ruby>に<ruby>踊<rt>おど</rt></ruby>ります。","dance","She dances well.","Verb"],
  ["chụp ảnh","Chụp giúp tôi một tấm.","<ruby>写真<rt>しゃしん</rt></ruby>を<ruby>撮<rt>と</rt></ruby>る","<ruby>写真<rt>しゃしん</rt></ruby>を<ruby>一枚<rt>いちまい</rt></ruby><ruby>撮<rt>と</rt></ruby>ってください。","take photo","Please take a photo for me.","Verb"],
  ["xem","Tối nay xem phim không?","<ruby>見<rt>み</rt></ruby>る","<ruby>今晩<rt>こんばん</rt></ruby><ruby>映画<rt>えいが</rt></ruby>を<ruby>見<rt>み</rt></ruby>ますか?","watch","Shall we watch a movie tonight?","Verb"],
  ["nghe","Tôi đang nghe nhạc.","<ruby>聞<rt>き</rt></ruby>く","<ruby>音楽<rt>おんがく</rt></ruby>を<ruby>聞<rt>き</rt></ruby>いています。","listen","I'm listening to music.","Verb"],
  ["mở","Mở cửa giúp tôi.","<ruby>開<rt>あ</rt></ruby>ける","ドアを<ruby>開<rt>あ</rt></ruby>けてください。","open","Please open the door.","Verb"],
  ["đóng","Đóng cửa lại.","<ruby>閉<rt>し</rt></ruby>める","ドアを<ruby>閉<rt>し</rt></ruby>めてください。","close","Close the door.","Verb"],
  ["bật","Bật đèn lên.","つける","<ruby>電気<rt>でんき</rt></ruby>をつけてください。","turn on","Turn on the light.","Verb"],
  ["tắt","Tắt máy lạnh.","<ruby>消<rt>け</rt></ruby>す","エアコンを<ruby>消<rt>け</rt></ruby>してください。","turn off","Turn off the AC.","Verb"],
  ["dạy","Cô giáo dạy tiếng Việt.","<ruby>教<rt>おし</rt></ruby>える","<ruby>先生<rt>せんせい</rt></ruby>がベトナム<ruby>語<rt>ご</rt></ruby>を<ruby>教<rt>おし</rt></ruby>えます。","teach","The teacher teaches Vietnamese.","Verb"],
  ["lái","Anh ấy lái xe rất giỏi.","<ruby>運転<rt>うんてん</rt></ruby>する","<ruby>彼<rt>かれ</rt></ruby>は<ruby>運転<rt>うんてん</rt></ruby>が<ruby>上手<rt>じょうず</rt></ruby>です。","drive","He drives very well.","Verb"],
  ["đi bộ","Tôi đi bộ đến công ty.","<ruby>歩<rt>ある</rt></ruby>く","<ruby>会社<rt>かいしゃ</rt></ruby>まで<ruby>歩<rt>ある</rt></ruby>きます。","walk","I walk to work.","Verb"],
  ["chạy bộ","Sáng nào tôi cũng chạy bộ.","ジョギングする","<ruby>毎朝<rt>まいあさ</rt></ruby>ジョギングします。","jog","I jog every morning.","Verb"],
  ["leo","Chúng tôi leo núi.","<ruby>登<rt>のぼ</rt></ruby>る","<ruby>山<rt>やま</rt></ruby>に<ruby>登<rt>のぼ</rt></ruby>ります。","climb","We climb the mountain.","Verb"],
  ["ngồi","Mời ngồi.","<ruby>座<rt>すわ</rt></ruby>る","お<ruby>座<rt>すわ</rt></ruby>りください。","sit","Please sit down.","Verb"],
  ["đứng","Đứng dậy đi.","<ruby>立<rt>た</rt></ruby>つ","<ruby>立<rt>た</rt></ruby>ってください。","stand","Please stand up.","Verb"],
  ["nằm","Tôi muốn nằm xuống.","<ruby>横<rt>よこ</rt></ruby>になる","<ruby>横<rt>よこ</rt></ruby>になりたいです。","lie down","I want to lie down.","Verb"],
  ["mặc","Em mặc áo dài rất đẹp.","<ruby>着<rt>き</rt></ruby>る","アオザイを<ruby>着<rt>き</rt></ruby>るととても<ruby>綺麗<rt>きれい</rt></ruby>です。","wear","You look pretty in ao dai.","Verb"],
  ["cởi","Cởi giày khi vào nhà.","<ruby>脱<rt>ぬ</rt></ruby>ぐ","<ruby>家<rt>いえ</rt></ruby>に<ruby>入<rt>はい</rt></ruby>るとき<ruby>靴<rt>くつ</rt></ruby>を<ruby>脱<rt>ぬ</rt></ruby>ぎます。","take off","Take off shoes when entering.","Verb"],
  ["ký","Hãy ký tên ở đây.","サインする","ここにサインしてください。","sign","Please sign here.","Verb"],
  ["chuyển","Tôi đã chuyển nhà.","<ruby>引<rt>ひ</rt></ruby>っ<ruby>越<rt>こ</rt></ruby>す","<ruby>引<rt>ひ</rt></ruby>っ<ruby>越<rt>こ</rt></ruby>しました。","move","I moved house.","Verb"],
  ["sửa","Cần sửa cái này.","<ruby>修理<rt>しゅうり</rt></ruby>する","これを<ruby>修理<rt>しゅうり</rt></ruby>する<ruby>必要<rt>ひつよう</rt></ruby>があります。","repair","Need to fix this.","Verb"],
  ["xây","Họ đang xây nhà mới.","<ruby>建<rt>た</rt></ruby>てる","<ruby>新<rt>あたら</rt></ruby>しい<ruby>家<rt>いえ</rt></ruby>を<ruby>建<rt>た</rt></ruby>てています。","build","They're building a new house.","Verb"],
  ["thắng","Đội nhà đã thắng.","<ruby>勝<rt>か</rt></ruby>つ","ホームチームが<ruby>勝<rt>か</rt></ruby>ちました。","win","The home team won.","Verb"],
  ["thua","Chúng tôi đã thua.","<ruby>負<rt>ま</rt></ruby>ける","<ruby>負<rt>ま</rt></ruby>けました。","lose","We lost.","Verb"],
  ["mượn","Cho mượn cái bút.","<ruby>借<rt>か</rt></ruby>りる","ペンを<ruby>貸<rt>か</rt></ruby>してください。","borrow","Lend me a pen.","Verb"],
  ["trả","Mai tôi trả lại.","<ruby>返<rt>かえ</rt></ruby>す","<ruby>明日<rt>あした</rt></ruby><ruby>返<rt>かえ</rt></ruby>します。","return","I'll return it tomorrow.","Verb"],
  ["chia sẻ","Hãy chia sẻ với mọi người.","<ruby>共有<rt>きょうゆう</rt></ruby>する","みんなと<ruby>共有<rt>きょうゆう</rt></ruby>してください。","share","Share with everyone.","Verb"],
  ["giúp","Bạn có thể giúp tôi không?","<ruby>手伝<rt>てつだ</rt></ruby>う","<ruby>手伝<rt>てつだ</rt></ruby>ってもらえますか?","help","Can you help me?","Verb"],
  ["thử","Cho tôi thử cái này.","<ruby>試<rt>ため</rt></ruby>す","これを<ruby>試<rt>ため</rt></ruby>させてください。","try","Let me try this.","Verb"],
  ["chuẩn bị","Tôi đang chuẩn bị bữa tối.","<ruby>準備<rt>じゅんび</rt></ruby>する","<ruby>夕食<rt>ゆうしょく</rt></ruby>を<ruby>準備<rt>じゅんび</rt></ruby>しています。","prepare","I'm preparing dinner.","Verb"],
  ["xin","Xin chỉ giúp đường.","<ruby>頼<rt>たの</rt></ruby>む","<ruby>道<rt>みち</rt></ruby>を<ruby>教<rt>おし</rt></ruby>えてください。","ask/request","Please tell me the way.","Verb"],
  ["đọc","Tôi đang đọc sách.","<ruby>読<rt>よ</rt></ruby>む","<ruby>本<rt>ほん</rt></ruby>を<ruby>読<rt>よ</rt></ruby>んでいます。","read","I'm reading a book.","Verb"],
  ["viết","Em viết tên đây nhé.","<ruby>書<rt>か</rt></ruby>く","ここに<ruby>名前<rt>なまえ</rt></ruby>を<ruby>書<rt>か</rt></ruby>いてください。","write","Write your name here.","Verb"],
  ["chơi","Trẻ em đang chơi.","<ruby>遊<rt>あそ</rt></ruby>ぶ","<ruby>子供<rt>こども</rt></ruby>たちが<ruby>遊<rt>あそ</rt></ruby>んでいます。","play","Children are playing.","Verb"],

  # ── Adjectives (35) ─────────────────────────────────────────
  ["nhanh","Anh ấy chạy nhanh.","<ruby>速<rt>はや</rt></ruby>い","<ruby>彼<rt>かれ</rt></ruby>は<ruby>速<rt>はや</rt></ruby>く<ruby>走<rt>はし</rt></ruby>ります。","fast","He runs fast.","Adjective"],
  ["chậm","Chậm thôi.","<ruby>遅<rt>おそ</rt></ruby>い","ゆっくりしてください。","slow","Slow down.","Adjective"],
  ["mạnh","Cà phê này mạnh quá.","<ruby>強<rt>つよ</rt></ruby>い","このコーヒーは<ruby>強<rt>つよ</rt></ruby>すぎます。","strong","This coffee is too strong.","Adjective"],
  ["yếu","Tôi cảm thấy yếu.","<ruby>弱<rt>よわ</rt></ruby>い","<ruby>弱<rt>よわ</rt></ruby>く<ruby>感<rt>かん</rt></ruby>じます。","weak","I feel weak.","Adjective"],
  ["dày","Quyển sách này dày.","<ruby>厚<rt>あつ</rt></ruby>い","この<ruby>本<rt>ほん</rt></ruby>は<ruby>厚<rt>あつ</rt></ruby>いです。","thick","This book is thick.","Adjective"],
  ["mỏng","Tờ giấy mỏng.","<ruby>薄<rt>うす</rt></ruby>い","<ruby>紙<rt>かみ</rt></ruby>は<ruby>薄<rt>うす</rt></ruby>いです。","thin","The paper is thin.","Adjective"],
  ["rộng","Phòng này rộng.","<ruby>広<rt>ひろ</rt></ruby>い","この<ruby>部屋<rt>へや</rt></ruby>は<ruby>広<rt>ひろ</rt></ruby>いです。","wide/spacious","This room is spacious.","Adjective"],
  ["hẹp","Đường hẹp.","<ruby>狭<rt>せま</rt></ruby>い","<ruby>道<rt>みち</rt></ruby>が<ruby>狭<rt>せま</rt></ruby>いです。","narrow","The road is narrow.","Adjective"],
  ["sâu","Hồ sâu lắm.","<ruby>深<rt>ふか</rt></ruby>い","<ruby>湖<rt>みずうみ</rt></ruby>はとても<ruby>深<rt>ふか</rt></ruby>いです。","deep","The lake is very deep.","Adjective"],
  ["nông","Sông cạn quá.","<ruby>浅<rt>あさ</rt></ruby>い","<ruby>川<rt>かわ</rt></ruby>は<ruby>浅<rt>あさ</rt></ruby>いです。","shallow","The river is shallow.","Adjective"],
  ["ướt","Áo bị ướt rồi.","<ruby>濡<rt>ぬ</rt></ruby>れた","<ruby>服<rt>ふく</rt></ruby>が<ruby>濡<rt>ぬ</rt></ruby>れました。","wet","The clothes are wet.","Adjective"],
  ["khô","Không khí khô lắm.","<ruby>乾<rt>かわ</rt></ruby>いた","<ruby>空気<rt>くうき</rt></ruby>が<ruby>乾燥<rt>かんそう</rt></ruby>しています。","dry","The air is dry.","Adjective"],
  ["mềm","Bánh mềm và ngon.","<ruby>柔<rt>やわ</rt></ruby>らかい","パンが<ruby>柔<rt>やわ</rt></ruby>らかくて<ruby>美味<rt>おい</rt></ruby>しいです。","soft","The bread is soft and tasty.","Adjective"],
  ["cứng","Đá cứng.","<ruby>硬<rt>かた</rt></ruby>い","<ruby>石<rt>いし</rt></ruby>は<ruby>硬<rt>かた</rt></ruby>いです。","hard","The stone is hard.","Adjective"],
  ["sạch","Phòng tôi rất sạch.","<ruby>清潔<rt>せいけつ</rt></ruby>","<ruby>私<rt>わたし</rt></ruby>の<ruby>部屋<rt>へや</rt></ruby>はとても<ruby>清潔<rt>せいけつ</rt></ruby>です。","clean","My room is very clean.","Adjective"],
  ["sáng","Phòng sáng quá.","<ruby>明<rt>あか</rt></ruby>るい","<ruby>部屋<rt>へや</rt></ruby>が<ruby>明<rt>あか</rt></ruby>るすぎます。","bright","The room is too bright.","Adjective"],
  ["tối","Ngoài trời tối rồi.","<ruby>暗<rt>くら</rt></ruby>い","<ruby>外<rt>そと</rt></ruby>は<ruby>暗<rt>くら</rt></ruby>くなりました。","dark","It's dark outside now.","Adjective"],
  ["cũ","Xe này cũ rồi.","<ruby>古<rt>ふる</rt></ruby>い","この<ruby>車<rt>くるま</rt></ruby>は<ruby>古<rt>ふる</rt></ruby>いです。","old","This car is old.","Adjective"],
  ["trẻ","Anh trẻ thật.","<ruby>若<rt>わか</rt></ruby>い","<ruby>本当<rt>ほんとう</rt></ruby>に<ruby>若<rt>わか</rt></ruby>いですね。","young","You're really young.","Adjective"],
  ["già","Bà tôi đã già.","<ruby>年<rt>とし</rt></ruby>を<ruby>取<rt>と</rt></ruby>った","<ruby>祖母<rt>そぼ</rt></ruby>は<ruby>年<rt>とし</rt></ruby>を<ruby>取<rt>と</rt></ruby>りました。","old (age)","My grandma is old.","Adjective"],
  ["mới","Điện thoại mới.","<ruby>新<rt>あたら</rt></ruby>しい","<ruby>新<rt>あたら</rt></ruby>しい<ruby>携帯<rt>けいたい</rt></ruby>です。","new","New phone.","Adjective"],
  ["thông minh","Em bé thông minh.","<ruby>賢<rt>かしこ</rt></ruby>い","<ruby>子供<rt>こども</rt></ruby>は<ruby>賢<rt>かしこ</rt></ruby>いです。","smart","The child is smart.","Adjective"],
  ["dễ thương","Mèo dễ thương quá.","<ruby>可愛<rt>かわい</rt></ruby>い","<ruby>猫<rt>ねこ</rt></ruby>はとても<ruby>可愛<rt>かわい</rt></ruby>いです。","cute","The cat is so cute.","Adjective"],
  ["đáng sợ","Phim đáng sợ.","<ruby>恐<rt>おそ</rt></ruby>ろしい","<ruby>恐<rt>おそ</rt></ruby>ろしい<ruby>映画<rt>えいが</rt></ruby>です。","scary","Scary movie.","Adjective"],
  ["lạ","Vị này lạ.","<ruby>変<rt>へん</rt></ruby>な","<ruby>変<rt>へん</rt></ruby>な<ruby>味<rt>あじ</rt></ruby>です。","strange","Strange taste.","Adjective"],
  ["quen","Mặt anh quen quá.","<ruby>馴染<rt>なじ</rt></ruby>みのある","あなたの<ruby>顔<rt>かお</rt></ruby>は<ruby>馴染<rt>なじ</rt></ruby>みがあります。","familiar","Your face is familiar.","Adjective"],
  ["nổi tiếng","Quán này nổi tiếng.","<ruby>有名<rt>ゆうめい</rt></ruby>","この<ruby>店<rt>みせ</rt></ruby>は<ruby>有名<rt>ゆうめい</rt></ruby>です。","famous","This shop is famous.","Adjective"],
  ["an toàn","Đây là nơi an toàn.","<ruby>安全<rt>あんぜん</rt></ruby>","ここは<ruby>安全<rt>あんぜん</rt></ruby>な<ruby>場所<rt>ばしょ</rt></ruby>です。","safe","This place is safe.","Adjective"],
  ["nguy hiểm","Đường nguy hiểm.","<ruby>危険<rt>きけん</rt></ruby>","<ruby>危険<rt>きけん</rt></ruby>な<ruby>道<rt>みち</rt></ruby>です。","dangerous","Dangerous road.","Adjective"],
  ["yên tĩnh","Phòng yên tĩnh.","<ruby>静<rt>しず</rt></ruby>か","<ruby>静<rt>しず</rt></ruby>かな<ruby>部屋<rt>へや</rt></ruby>です。","quiet","Quiet room.","Adjective"],
  ["ồn","Quán ồn quá.","うるさい","<ruby>店<rt>みせ</rt></ruby>がうるさいです。","noisy","The shop is too noisy.","Adjective"],
  ["thoải mái","Cảm thấy thoải mái.","<ruby>快適<rt>かいてき</rt></ruby>","<ruby>快適<rt>かいてき</rt></ruby>に<ruby>感<rt>かん</rt></ruby>じます。","comfortable","I feel comfortable.","Adjective"],
  ["bất tiện","Nhà ga bất tiện.","<ruby>不便<rt>ふべん</rt></ruby>","<ruby>駅<rt>えき</rt></ruby>は<ruby>不便<rt>ふべん</rt></ruby>です。","inconvenient","The station is inconvenient.","Adjective"],
  ["rảnh","Chiều nay tôi rảnh.","<ruby>暇<rt>ひま</rt></ruby>","<ruby>今日<rt>きょう</rt></ruby>の<ruby>午後<rt>ごご</rt></ruby>は<ruby>暇<rt>ひま</rt></ruby>です。","free","I'm free this afternoon.","Adjective"],
  ["rất","Rất cảm ơn.","とても","とてもありがとう。","very","Thank you very much.","Adjective"],

  # ── Time/Date (20) ──────────────────────────────────────────
  ["sáng","Buổi sáng tôi uống cà phê.","<ruby>朝<rt>あさ</rt></ruby>","<ruby>朝<rt>あさ</rt></ruby>コーヒーを<ruby>飲<rt>の</rt></ruby>みます。","morning","I drink coffee in the morning.","Time"],
  ["trưa","Trưa nay ăn gì?","<ruby>昼<rt>ひる</rt></ruby>","<ruby>昼<rt>ひる</rt></ruby>に<ruby>何<rt>なに</rt></ruby>を<ruby>食<rt>た</rt></ruby>べますか?","noon","What's for lunch today?","Time"],
  ["tối","Tối nay đi ăn không?","<ruby>夜<rt>よる</rt></ruby>","<ruby>今夜<rt>こんや</rt></ruby><ruby>食事<rt>しょくじ</rt></ruby>に<ruby>行<rt>い</rt></ruby>きませんか?","evening/night","Shall we eat tonight?","Time"],
  ["khuya","Đừng thức khuya quá.","<ruby>夜遅<rt>よるおそ</rt></ruby>く","<ruby>夜遅<rt>よるおそ</rt></ruby>くまで<ruby>起<rt>お</rt></ruby>きないで。","late night","Don't stay up too late.","Time"],
  ["sớm","Tôi dậy sớm.","<ruby>早<rt>はや</rt></ruby>く","<ruby>早<rt>はや</rt></ruby>く<ruby>起<rt>お</rt></ruby>きます。","early","I wake up early.","Time"],
  ["muộn","Đến muộn rồi.","<ruby>遅<rt>おそ</rt></ruby>く","<ruby>遅<rt>おそ</rt></ruby>く<ruby>来<rt>き</rt></ruby>ました。","late","I arrived late.","Time"],
  ["thứ hai","Thứ hai có họp.","<ruby>月曜日<rt>げつようび</rt></ruby>","<ruby>月曜日<rt>げつようび</rt></ruby>に<ruby>会議<rt>かいぎ</rt></ruby>があります。","Monday","Meeting on Monday.","Time"],
  ["thứ ba","Thứ ba tôi rảnh.","<ruby>火曜日<rt>かようび</rt></ruby>","<ruby>火曜日<rt>かようび</rt></ruby>は<ruby>暇<rt>ひま</rt></ruby>です。","Tuesday","I'm free on Tuesday.","Time"],
  ["thứ tư","Thứ tư đi học.","<ruby>水曜日<rt>すいようび</rt></ruby>","<ruby>水曜日<rt>すいようび</rt></ruby>に<ruby>学校<rt>がっこう</rt></ruby>に<ruby>行<rt>い</rt></ruby>きます。","Wednesday","School on Wednesday.","Time"],
  ["thứ năm","Thứ năm đi tập.","<ruby>木曜日<rt>もくようび</rt></ruby>","<ruby>木曜日<rt>もくようび</rt></ruby>に<ruby>運動<rt>うんどう</rt></ruby>します。","Thursday","Workout on Thursday.","Time"],
  ["thứ sáu","Thứ sáu đi nhậu nhé.","<ruby>金曜日<rt>きんようび</rt></ruby>","<ruby>金曜日<rt>きんようび</rt></ruby>に<ruby>飲<rt>の</rt></ruby>みに<ruby>行<rt>い</rt></ruby>きましょう。","Friday","Let's go drinking Friday.","Time"],
  ["thứ bảy","Thứ bảy đi chơi.","<ruby>土曜日<rt>どようび</rt></ruby>","<ruby>土曜日<rt>どようび</rt></ruby>に<ruby>遊<rt>あそ</rt></ruby>びに<ruby>行<rt>い</rt></ruby>きます。","Saturday","Going out on Saturday.","Time"],
  ["chủ nhật","Chủ nhật nghỉ.","<ruby>日曜日<rt>にちようび</rt></ruby>","<ruby>日曜日<rt>にちようび</rt></ruby>は<ruby>休<rt>やす</rt></ruby>みです。","Sunday","Sunday is off.","Time"],
  ["mùa xuân","Mùa xuân ấm áp.","<ruby>春<rt>はる</rt></ruby>","<ruby>春<rt>はる</rt></ruby>は<ruby>暖<rt>あたた</rt></ruby>かいです。","spring","Spring is warm.","Time"],
  ["mùa hè","Mùa hè rất nóng.","<ruby>夏<rt>なつ</rt></ruby>","<ruby>夏<rt>なつ</rt></ruby>はとても<ruby>暑<rt>あつ</rt></ruby>いです。","summer","Summer is very hot.","Time"],
  ["mùa thu","Mùa thu mát mẻ.","<ruby>秋<rt>あき</rt></ruby>","<ruby>秋<rt>あき</rt></ruby>は<ruby>涼<rt>すず</rt></ruby>しいです。","autumn","Autumn is cool.","Time"],
  ["mùa đông","Mùa đông lạnh lắm.","<ruby>冬<rt>ふゆ</rt></ruby>","<ruby>冬<rt>ふゆ</rt></ruby>はとても<ruby>寒<rt>さむ</rt></ruby>いです。","winter","Winter is very cold.","Time"],
  ["năm ngoái","Năm ngoái tôi đến Việt Nam.","<ruby>去年<rt>きょねん</rt></ruby>","<ruby>去年<rt>きょねん</rt></ruby>ベトナムに<ruby>来<rt>き</rt></ruby>ました。","last year","Last year I came to Vietnam.","Time"],
  ["năm sau","Năm sau tôi sẽ kết hôn.","<ruby>来年<rt>らいねん</rt></ruby>","<ruby>来年<rt>らいねん</rt></ruby><ruby>結婚<rt>けっこん</rt></ruby>します。","next year","I'll marry next year.","Time"],
  ["lần sau","Hẹn lần sau nhé.","<ruby>次回<rt>じかい</rt></ruby>","<ruby>次回<rt>じかい</rt></ruby>また。","next time","See you next time.","Time"],

  # ── Numbers (10) ────────────────────────────────────────────
  ["mười một","Tôi có mười một quyển sách.","<ruby>十一<rt>じゅういち</rt></ruby>","<ruby>本<rt>ほん</rt></ruby>を<ruby>十一冊<rt>じゅういっさつ</rt></ruby><ruby>持<rt>も</rt></ruby>っています。","eleven","I have 11 books.","Number"],
  ["mười hai","Mười hai tháng một năm.","<ruby>十二<rt>じゅうに</rt></ruby>","<ruby>一年<rt>いちねん</rt></ruby>は<ruby>十二<rt>じゅうに</rt></ruby>か<ruby>月<rt>げつ</rt></ruby>です。","twelve","12 months in a year.","Number"],
  ["hai mươi","Tôi hai mươi tuổi.","<ruby>二十<rt>にじゅう</rt></ruby>","<ruby>二十歳<rt>はたち</rt></ruby>です。","twenty","I'm 20 years old.","Number"],
  ["ba mươi","Tháng có ba mươi ngày.","<ruby>三十<rt>さんじゅう</rt></ruby>","<ruby>一<rt>いち</rt></ruby>か<ruby>月<rt>げつ</rt></ruby>は<ruby>三十日<rt>さんじゅうにち</rt></ruby>です。","thirty","30 days in a month.","Number"],
  ["năm mươi","Năm mươi phần trăm.","<ruby>五十<rt>ごじゅう</rt></ruby>","<ruby>五十<rt>ごじゅう</rt></ruby>パーセント。","fifty","50 percent.","Number"],
  ["năm trăm","Năm trăm nghìn đồng.","<ruby>五百<rt>ごひゃく</rt></ruby>","<ruby>五十万<rt>ごじゅうまん</rt></ruby>ドン。","five hundred","500,000 dong.","Number"],
  ["nửa","Một nửa cái bánh.","<ruby>半分<rt>はんぶん</rt></ruby>","ケーキの<ruby>半分<rt>はんぶん</rt></ruby>。","half","Half a cake.","Number"],
  ["đôi","Một đôi giày.","<ruby>一足<rt>いっそく</rt></ruby> / ペア","<ruby>靴<rt>くつ</rt></ruby><ruby>一足<rt>いっそく</rt></ruby>。","pair","A pair of shoes.","Number"],
  ["chục","Một chục trứng.","<ruby>十個<rt>じっこ</rt></ruby>","<ruby>卵<rt>たまご</rt></ruby><ruby>十個<rt>じっこ</rt></ruby>。","ten/dozen","Ten eggs.","Number"],
  ["lần","Tôi đi ba lần.","<ruby>回<rt>かい</rt></ruby>","<ruby>三回<rt>さんかい</rt></ruby><ruby>行<rt>い</rt></ruby>きます。","time(s)","I go three times.","Number"],

  # ── Pronouns/Question (5+5=10) ──────────────────────────────
  ["mình","Mình đi nhé.","<ruby>自分<rt>じぶん</rt></ruby> / <ruby>私<rt>わたし</rt></ruby>","<ruby>私<rt>わたし</rt></ruby><ruby>行<rt>い</rt></ruby>くね。","I (intimate)","I'm going.","Pronoun"],
  ["tớ","Tớ tên là Linh.","<ruby>僕<rt>ぼく</rt></ruby> / <ruby>私<rt>わたし</rt></ruby>","<ruby>私<rt>わたし</rt></ruby>はリンです。","I (casual)","My name is Linh.","Pronoun"],
  ["cậu","Cậu khỏe không?","<ruby>君<rt>きみ</rt></ruby>","<ruby>君<rt>きみ</rt></ruby>、<ruby>元気<rt>げんき</rt></ruby>?","you (casual)","How are you?","Pronoun"],
  ["họ","Họ là bạn tôi.","<ruby>彼<rt>かれ</rt></ruby>ら","<ruby>彼<rt>かれ</rt></ruby>らは<ruby>友達<rt>ともだち</rt></ruby>です。","they","They are my friends.","Pronoun"],
  ["mọi người","Chào mọi người.","みなさん","みなさん、こんにちは。","everyone","Hello everyone.","Pronoun"],
  ["thế nào","Anh thế nào?","どう","どうですか?","how","How are you?","Question"],
  ["mấy","Mấy giờ rồi?","<ruby>何<rt>なん</rt></ruby>","<ruby>何時<rt>なんじ</rt></ruby>ですか?","what (number)","What time is it?","Question"],
  ["nào","Cái nào?","どれ","どれですか?","which","Which one?","Question"],
  ["hay","Cái này hay không?","それとも","それともどちら?","or","This or that?","Question"],
  ["thật không","Thật không?","<ruby>本当<rt>ほんとう</rt></ruby>?","<ruby>本当<rt>ほんとう</rt></ruby>ですか?","really?","Really?","Question"],

  # ── Greetings/Phrases (8) ───────────────────────────────────
  ["không sao","Không sao đâu.","<ruby>大丈夫<rt>だいじょうぶ</rt></ruby>","<ruby>大丈夫<rt>だいじょうぶ</rt></ruby>ですよ。","no problem","It's okay.","Greeting"],
  ["chúc mừng","Chúc mừng sinh nhật.","おめでとう","お<ruby>誕生日<rt>たんじょうび</rt></ruby>おめでとう。","congratulations","Happy birthday.","Greeting"],
  ["chúc ngủ ngon","Chúc ngủ ngon.","おやすみなさい","おやすみなさい。","good night","Good night.","Greeting"],
  ["xin mời","Xin mời vào.","どうぞ","どうぞ<ruby>入<rt>はい</rt></ruby>ってください。","please (welcome)","Please come in.","Greeting"],
  ["cảm ơn nhiều","Cảm ơn nhiều ạ.","どうもありがとう","どうもありがとうございます。","thanks a lot","Thank you very much.","Greeting"],
  ["xin lỗi nhé","Xin lỗi nhé.","ごめんね","ごめんね。","sorry","Sorry.","Greeting"],
  ["nhờ","Nhờ anh giúp.","お<ruby>願<rt>ねが</rt></ruby>いします","お<ruby>願<rt>ねが</rt></ruby>いします。","please help","Please help me.","Greeting"],
  ["lâu rồi","Lâu rồi không gặp.","<ruby>久<rt>ひさ</rt></ruby>しぶり","お<ruby>久<rt>ひさ</rt></ruby>しぶりです。","long time","Long time no see.","Greeting"],

  # ── Body parts (25) ─────────────────────────────────────────
  ["đầu","Tôi đau đầu.","<ruby>頭<rt>あたま</rt></ruby>","<ruby>頭<rt>あたま</rt></ruby>が<ruby>痛<rt>いた</rt></ruby>いです。","head","I have a headache.","Noun"],
  ["mặt","Rửa mặt đi.","<ruby>顔<rt>かお</rt></ruby>","<ruby>顔<rt>かお</rt></ruby>を<ruby>洗<rt>あら</rt></ruby>ってください。","face","Wash your face.","Noun"],
  ["mắt","Mắt em đẹp.","<ruby>目<rt>め</rt></ruby>","<ruby>目<rt>め</rt></ruby>がきれいです。","eye","Beautiful eyes.","Noun"],
  ["tai","Đeo tai nghe vào.","<ruby>耳<rt>みみ</rt></ruby>","イヤホンをつけてください。","ear","Put on the earphones.","Noun"],
  ["mũi","Mũi cao.","<ruby>鼻<rt>はな</rt></ruby>","<ruby>鼻<rt>はな</rt></ruby>が<ruby>高<rt>たか</rt></ruby>いです。","nose","High nose.","Noun"],
  ["miệng","Mở miệng ra.","<ruby>口<rt>くち</rt></ruby>","<ruby>口<rt>くち</rt></ruby>を<ruby>開<rt>あ</rt></ruby>けてください。","mouth","Open your mouth.","Noun"],
  ["răng","Răng tôi đau.","<ruby>歯<rt>は</rt></ruby>","<ruby>歯<rt>は</rt></ruby>が<ruby>痛<rt>いた</rt></ruby>いです。","tooth","My tooth hurts.","Noun"],
  ["lưỡi","Le lưỡi.","<ruby>舌<rt>した</rt></ruby>","<ruby>舌<rt>した</rt></ruby>を<ruby>出<rt>だ</rt></ruby>す。","tongue","Stick out tongue.","Noun"],
  ["cổ","Cổ tôi mỏi.","<ruby>首<rt>くび</rt></ruby>","<ruby>首<rt>くび</rt></ruby>が<ruby>疲<rt>つか</rt></ruby>れます。","neck","My neck is tired.","Noun"],
  ["vai","Vai mỏi quá.","<ruby>肩<rt>かた</rt></ruby>","<ruby>肩<rt>かた</rt></ruby>がこっています。","shoulder","Stiff shoulders.","Noun"],
  ["tay","Đưa tay đây.","<ruby>手<rt>て</rt></ruby>","<ruby>手<rt>て</rt></ruby>を<ruby>出<rt>だ</rt></ruby>してください。","hand","Give me your hand.","Noun"],
  ["chân","Chân tôi đau.","<ruby>足<rt>あし</rt></ruby>","<ruby>足<rt>あし</rt></ruby>が<ruby>痛<rt>いた</rt></ruby>いです。","leg/foot","My leg hurts.","Noun"],
  ["ngón tay","Ngón tay bị đứt.","<ruby>指<rt>ゆび</rt></ruby>","<ruby>指<rt>ゆび</rt></ruby>を<ruby>切<rt>き</rt></ruby>りました。","finger","I cut my finger.","Noun"],
  ["lưng","Lưng đau quá.","<ruby>背中<rt>せなか</rt></ruby>","<ruby>背中<rt>せなか</rt></ruby>が<ruby>痛<rt>いた</rt></ruby>いです。","back","My back hurts.","Noun"],
  ["bụng","Bụng đói.","お<ruby>腹<rt>なか</rt></ruby>","お<ruby>腹<rt>なか</rt></ruby>が<ruby>空<rt>す</rt></ruby>きました。","stomach","I'm hungry.","Noun"],
  ["tim","Tim đập nhanh.","<ruby>心臓<rt>しんぞう</rt></ruby>","<ruby>心臓<rt>しんぞう</rt></ruby>がドキドキします。","heart","My heart is racing.","Noun"],
  ["máu","Bị chảy máu.","<ruby>血<rt>ち</rt></ruby>","<ruby>血<rt>ち</rt></ruby>が<ruby>出<rt>で</rt></ruby>ました。","blood","Bleeding.","Noun"],
  ["xương","Gãy xương.","<ruby>骨<rt>ほね</rt></ruby>","<ruby>骨折<rt>こっせつ</rt></ruby>しました。","bone","Broken bone.","Noun"],
  ["da","Da khô.","<ruby>肌<rt>はだ</rt></ruby>","<ruby>肌<rt>はだ</rt></ruby>が<ruby>乾燥<rt>かんそう</rt></ruby>しています。","skin","Dry skin.","Noun"],
  ["tóc","Tóc dài.","<ruby>髪<rt>かみ</rt></ruby>","<ruby>髪<rt>かみ</rt></ruby>が<ruby>長<rt>なが</rt></ruby>いです。","hair","Long hair.","Noun"],
  ["sức khỏe","Sức khỏe quan trọng.","<ruby>健康<rt>けんこう</rt></ruby>","<ruby>健康<rt>けんこう</rt></ruby>は<ruby>大事<rt>だいじ</rt></ruby>です。","health","Health matters.","Noun"],
  ["đau","Tôi bị đau.","<ruby>痛<rt>いた</rt></ruby>い","<ruby>痛<rt>いた</rt></ruby>いです。","pain","I'm in pain.","Adjective"],
  ["bệnh","Bệnh nặng quá.","<ruby>病気<rt>びょうき</rt></ruby>","<ruby>重<rt>おも</rt></ruby>い<ruby>病気<rt>びょうき</rt></ruby>です。","illness","Serious illness.","Noun"],
  ["thuốc","Uống thuốc đi.","<ruby>薬<rt>くすり</rt></ruby>","<ruby>薬<rt>くすり</rt></ruby>を<ruby>飲<rt>の</rt></ruby>んでください。","medicine","Take medicine.","Noun"],
  ["bệnh viện","Đến bệnh viện ngay.","<ruby>病院<rt>びょういん</rt></ruby>","<ruby>病院<rt>びょういん</rt></ruby>に<ruby>行<rt>い</rt></ruby>ってください。","hospital","Go to the hospital.","Noun"],

  # ── Family (20) ─────────────────────────────────────────────
  ["bố","Bố tôi đi làm.","<ruby>父<rt>ちち</rt></ruby>","<ruby>父<rt>ちち</rt></ruby>は<ruby>仕事<rt>しごと</rt></ruby>に<ruby>行<rt>い</rt></ruby>きます。","father","My father goes to work.","Noun"],
  ["mẹ","Mẹ nấu ăn ngon.","<ruby>母<rt>はは</rt></ruby>","<ruby>母<rt>はは</rt></ruby>は<ruby>料理<rt>りょうり</rt></ruby>が<ruby>上手<rt>じょうず</rt></ruby>です。","mother","Mom cooks well.","Noun"],
  ["con trai","Con trai tôi 5 tuổi.","<ruby>息子<rt>むすこ</rt></ruby>","<ruby>息子<rt>むすこ</rt></ruby>は5<ruby>歳<rt>さい</rt></ruby>です。","son","My son is 5.","Noun"],
  ["con gái","Con gái tôi đang học.","<ruby>娘<rt>むすめ</rt></ruby>","<ruby>娘<rt>むすめ</rt></ruby>は<ruby>勉強<rt>べんきょう</rt></ruby>しています。","daughter","My daughter is studying.","Noun"],
  ["anh trai","Anh trai tôi.","お<ruby>兄<rt>にい</rt></ruby>さん","お<ruby>兄<rt>にい</rt></ruby>さんです。","older brother","My older brother.","Noun"],
  ["em trai","Em trai tôi học giỏi.","<ruby>弟<rt>おとうと</rt></ruby>","<ruby>弟<rt>おとうと</rt></ruby>は<ruby>勉強<rt>べんきょう</rt></ruby>ができます。","younger brother","My brother studies well.","Noun"],
  ["chị gái","Chị gái tôi.","お<ruby>姉<rt>ねえ</rt></ruby>さん","お<ruby>姉<rt>ねえ</rt></ruby>さんです。","older sister","My older sister.","Noun"],
  ["em gái","Em gái tôi.","<ruby>妹<rt>いもうと</rt></ruby>","<ruby>妹<rt>いもうと</rt></ruby>です。","younger sister","My little sister.","Noun"],
  ["ông","Ông tôi 80 tuổi.","<ruby>祖父<rt>そふ</rt></ruby>","<ruby>祖父<rt>そふ</rt></ruby>は80<ruby>歳<rt>さい</rt></ruby>です。","grandfather","Grandpa is 80.","Noun"],
  ["cháu","Cháu tôi rất ngoan.","<ruby>孫<rt>まご</rt></ruby>","<ruby>孫<rt>まご</rt></ruby>はお<ruby>利口<rt>りこう</rt></ruby>です。","grandchild","My grandchild is good.","Noun"],
  ["chú","Chú tôi sống ở Mỹ.","おじ","おじはアメリカに<ruby>住<rt>す</rt></ruby>んでいます。","uncle (paternal)","My uncle lives in US.","Noun"],
  ["cô","Cô là giáo viên.","おば / <ruby>先生<rt>せんせい</rt></ruby>","おばは<ruby>先生<rt>せんせい</rt></ruby>です。","aunt/teacher","She's a teacher/aunt.","Noun"],
  ["bác","Bác tôi đến chơi.","おじ・おば","おじが<ruby>遊<rt>あそ</rt></ruby>びに<ruby>来<rt>き</rt></ruby>ました。","uncle/aunt (older)","My uncle visited.","Noun"],
  ["dì","Dì rất tốt với tôi.","おば","おばはとても<ruby>優<rt>やさ</rt></ruby>しいです。","aunt (maternal)","My aunt is kind.","Noun"],
  ["cậu","Cậu tôi là thợ may.","おじ","おじは<ruby>仕立屋<rt>したてや</rt></ruby>です。","uncle (maternal)","My uncle is a tailor.","Noun"],
  ["anh em","Chúng tôi là anh em.","<ruby>兄弟<rt>きょうだい</rt></ruby>","<ruby>私<rt>わたし</rt></ruby>たちは<ruby>兄弟<rt>きょうだい</rt></ruby>です。","siblings","We are siblings.","Noun"],
  ["họ hàng","Họ hàng ở quê.","<ruby>親戚<rt>しんせき</rt></ruby>","<ruby>親戚<rt>しんせき</rt></ruby>は<ruby>田舎<rt>いなか</rt></ruby>にいます。","relatives","Relatives live in the countryside.","Noun"],
  ["bạn trai","Bạn trai tôi đẹp trai.","<ruby>彼氏<rt>かれし</rt></ruby>","<ruby>彼氏<rt>かれし</rt></ruby>はかっこいいです。","boyfriend","My boyfriend is handsome.","Noun"],
  ["bạn gái","Bạn gái tôi dễ thương.","<ruby>彼女<rt>かのじょ</rt></ruby>","<ruby>彼女<rt>かのじょ</rt></ruby>は<ruby>可愛<rt>かわい</rt></ruby>いです。","girlfriend","My girlfriend is cute.","Noun"],
  ["hàng xóm","Hàng xóm rất tốt.","<ruby>隣人<rt>りんじん</rt></ruby>","<ruby>隣人<rt>りんじん</rt></ruby>はとても<ruby>親切<rt>しんせつ</rt></ruby>です。","neighbor","Neighbor is kind.","Noun"],

  # ── Colors (12) ─────────────────────────────────────────────
  ["màu đỏ","Áo màu đỏ.","<ruby>赤<rt>あか</rt></ruby>","<ruby>赤<rt>あか</rt></ruby>い<ruby>服<rt>ふく</rt></ruby>。","red","Red clothes.","Adjective"],
  ["màu xanh dương","Trời màu xanh dương.","<ruby>青<rt>あお</rt></ruby>","<ruby>空<rt>そら</rt></ruby>は<ruby>青<rt>あお</rt></ruby>いです。","blue","The sky is blue.","Adjective"],
  ["màu xanh lá","Lá màu xanh lá.","<ruby>緑<rt>みどり</rt></ruby>","<ruby>葉<rt>は</rt></ruby>は<ruby>緑<rt>みどり</rt></ruby>です。","green","Leaves are green.","Adjective"],
  ["màu vàng","Hoa màu vàng.","<ruby>黄色<rt>きいろ</rt></ruby>","<ruby>黄色<rt>きいろ</rt></ruby>の<ruby>花<rt>はな</rt></ruby>。","yellow","Yellow flower.","Adjective"],
  ["màu đen","Tóc màu đen.","<ruby>黒<rt>くろ</rt></ruby>","<ruby>髪<rt>かみ</rt></ruby>は<ruby>黒<rt>くろ</rt></ruby>いです。","black","Black hair.","Adjective"],
  ["màu trắng","Áo màu trắng.","<ruby>白<rt>しろ</rt></ruby>","<ruby>白<rt>しろ</rt></ruby>い<ruby>服<rt>ふく</rt></ruby>。","white","White clothes.","Adjective"],
  ["màu hồng","Tôi thích màu hồng.","ピンク","ピンクが<ruby>好<rt>す</rt></ruby>きです。","pink","I like pink.","Adjective"],
  ["màu tím","Hoa màu tím đẹp.","<ruby>紫<rt>むらさき</rt></ruby>","<ruby>紫<rt>むらさき</rt></ruby>の<ruby>花<rt>はな</rt></ruby>がきれいです。","purple","Purple flowers are pretty.","Adjective"],
  ["màu cam","Cam màu cam.","オレンジ<ruby>色<rt>いろ</rt></ruby>","オレンジは<ruby>橙色<rt>だいだいいろ</rt></ruby>です。","orange","Orange is orange-colored.","Adjective"],
  ["màu xám","Trời màu xám.","<ruby>灰色<rt>はいいろ</rt></ruby>","<ruby>空<rt>そら</rt></ruby>は<ruby>灰色<rt>はいいろ</rt></ruby>です。","gray","The sky is gray.","Adjective"],
  ["màu nâu","Cà phê màu nâu.","<ruby>茶色<rt>ちゃいろ</rt></ruby>","コーヒーは<ruby>茶色<rt>ちゃいろ</rt></ruby>です。","brown","Coffee is brown.","Adjective"],
  ["màu","Bạn thích màu gì?","<ruby>色<rt>いろ</rt></ruby>","<ruby>何色<rt>なにいろ</rt></ruby>が<ruby>好<rt>す</rt></ruby>きですか?","color","What color do you like?","Noun"],

  # ── Weather (12) ────────────────────────────────────────────
  ["thời tiết","Thời tiết đẹp.","<ruby>天気<rt>てんき</rt></ruby>","<ruby>天気<rt>てんき</rt></ruby>がいいです。","weather","Nice weather.","Noun"],
  ["nắng","Hôm nay nắng.","<ruby>晴<rt>は</rt></ruby>れ","<ruby>今日<rt>きょう</rt></ruby>は<ruby>晴<rt>は</rt></ruby>れです。","sunny","Sunny today.","Adjective"],
  ["có mây","Trời có mây.","<ruby>曇<rt>くも</rt></ruby>り","<ruby>曇<rt>くも</rt></ruby>りです。","cloudy","Cloudy.","Adjective"],
  ["bão","Có bão lớn.","<ruby>台風<rt>たいふう</rt></ruby>","<ruby>大<rt>おお</rt></ruby>きい<ruby>台風<rt>たいふう</rt></ruby>です。","storm","Big storm.","Noun"],
  ["sấm","Có tiếng sấm.","<ruby>雷<rt>かみなり</rt></ruby>","<ruby>雷<rt>かみなり</rt></ruby>が<ruby>鳴<rt>な</rt></ruby>っています。","thunder","Thunder rumbles.","Noun"],
  ["sét","Sét đánh đáng sợ.","<ruby>稲妻<rt>いなずま</rt></ruby>","<ruby>稲妻<rt>いなずま</rt></ruby>が<ruby>怖<rt>こわ</rt></ruby>いです。","lightning","Lightning is scary.","Noun"],
  ["sương mù","Sáng nay có sương mù.","<ruby>霧<rt>きり</rt></ruby>","<ruby>今朝<rt>けさ</rt></ruby><ruby>霧<rt>きり</rt></ruby>がかかっています。","fog","Foggy this morning.","Noun"],
  ["tuyết","Hà Nội không có tuyết.","<ruby>雪<rt>ゆき</rt></ruby>","ハノイには<ruby>雪<rt>ゆき</rt></ruby>がありません。","snow","No snow in Hanoi.","Noun"],
  ["nhiệt độ","Nhiệt độ cao quá.","<ruby>温度<rt>おんど</rt></ruby>","<ruby>温度<rt>おんど</rt></ruby>が<ruby>高<rt>たか</rt></ruby>すぎます。","temperature","Too hot.","Noun"],
  ["ấm","Trời ấm dần.","<ruby>暖<rt>あたた</rt></ruby>かい","<ruby>暖<rt>あたた</rt></ruby>かくなってきました。","warm","Getting warmer.","Adjective"],
  ["mát","Buổi tối mát.","<ruby>涼<rt>すず</rt></ruby>しい","<ruby>夜<rt>よる</rt></ruby>は<ruby>涼<rt>すず</rt></ruby>しいです。","cool","Cool at night.","Adjective"],
  ["gió mạnh","Hôm nay gió mạnh.","<ruby>強風<rt>きょうふう</rt></ruby>","<ruby>今日<rt>きょう</rt></ruby>は<ruby>風<rt>かぜ</rt></ruby>が<ruby>強<rt>つよ</rt></ruby>いです。","strong wind","Strong wind today.","Adjective"],

  # ── Place (15) ──────────────────────────────────────────────
  ["thành phố","Thành phố Hồ Chí Minh.","<ruby>都市<rt>とし</rt></ruby>","ホーチミン<ruby>市<rt>し</rt></ruby>。","city","Ho Chi Minh City.","Noun"],
  ["quê","Tôi về quê dịp Tết.","<ruby>故郷<rt>こきょう</rt></ruby>","テトに<ruby>故郷<rt>こきょう</rt></ruby>へ<ruby>帰<rt>かえ</rt></ruby>ります。","hometown","I go home for Tet.","Noun"],
  ["đất nước","Đất nước Việt Nam đẹp.","<ruby>国<rt>くに</rt></ruby>","ベトナムは<ruby>美<rt>うつく</rt></ruby>しい<ruby>国<rt>くに</rt></ruby>です。","country","Vietnam is a beautiful country.","Noun"],
  ["thế giới","Đi khắp thế giới.","<ruby>世界<rt>せかい</rt></ruby>","<ruby>世界中<rt>せかいじゅう</rt></ruby>を<ruby>旅<rt>たび</rt></ruby>する。","world","Travel the world.","Noun"],
  ["công viên","Đi dạo trong công viên.","<ruby>公園<rt>こうえん</rt></ruby>","<ruby>公園<rt>こうえん</rt></ruby>を<ruby>散歩<rt>さんぽ</rt></ruby>する。","park","Walk in the park.","Noun"],
  ["chợ","Tôi đi chợ.","<ruby>市場<rt>いちば</rt></ruby>","<ruby>市場<rt>いちば</rt></ruby>に<ruby>行<rt>い</rt></ruby>きます。","market","I go to the market.","Noun"],
  ["siêu thị","Mua đồ ở siêu thị.","スーパー","スーパーで<ruby>買<rt>か</rt></ruby>い<ruby>物<rt>もの</rt></ruby>します。","supermarket","Shop at the supermarket.","Noun"],
  ["trung tâm","Trung tâm thành phố.","<ruby>中心<rt>ちゅうしん</rt></ruby>","<ruby>市<rt>し</rt></ruby>の<ruby>中心<rt>ちゅうしん</rt></ruby>。","center","City center.","Noun"],
  ["cửa hàng","Cửa hàng đóng cửa.","<ruby>店<rt>みせ</rt></ruby>","<ruby>店<rt>みせ</rt></ruby>が<ruby>閉<rt>し</rt></ruby>まっています。","shop","The shop is closed.","Noun"],
  ["tiệm cà phê","Tiệm cà phê đẹp.","カフェ","おしゃれなカフェです。","café","Nice café.","Noun"],
  ["quán nhậu","Quán nhậu đông khách.","<ruby>居酒屋<rt>いざかや</rt></ruby>","<ruby>居酒屋<rt>いざかや</rt></ruby>は<ruby>混<rt>こ</rt></ruby>んでいます。","pub","The pub is crowded.","Noun"],
  ["đại sứ quán","Đến đại sứ quán Hàn Quốc.","<ruby>大使館<rt>たいしかん</rt></ruby>","<ruby>韓国<rt>かんこく</rt></ruby><ruby>大使館<rt>たいしかん</rt></ruby>へ<ruby>行<rt>い</rt></ruby>きます。","embassy","Go to Korean embassy.","Noun"],
  ["toà nhà","Toà nhà cao tầng.","ビル","<ruby>高<rt>たか</rt></ruby>いビル。","building","Tall building.","Noun"],
  ["sân","Sân nhà rộng.","<ruby>庭<rt>にわ</rt></ruby>","<ruby>家<rt>いえ</rt></ruby>の<ruby>庭<rt>にわ</rt></ruby>は<ruby>広<rt>ひろ</rt></ruby>いです。","yard","Wide yard.","Noun"],
  ["bãi biển","Bãi biển Đà Nẵng đẹp.","ビーチ","ダナンのビーチはきれいです。","beach","Da Nang beach is beautiful.","Noun"],

  # ── Food/Drink (15) ─────────────────────────────────────────
  ["bữa sáng","Bữa sáng quan trọng.","<ruby>朝食<rt>ちょうしょく</rt></ruby>","<ruby>朝食<rt>ちょうしょく</rt></ruby>は<ruby>大事<rt>だいじ</rt></ruby>です。","breakfast","Breakfast is important.","Noun"],
  ["bữa trưa","Bữa trưa lúc 12 giờ.","<ruby>昼食<rt>ちゅうしょく</rt></ruby>","<ruby>昼食<rt>ちゅうしょく</rt></ruby>は12<ruby>時<rt>じ</rt></ruby>です。","lunch","Lunch at 12.","Noun"],
  ["bữa tối","Cùng ăn bữa tối.","<ruby>夕食<rt>ゆうしょく</rt></ruby>","<ruby>一緒<rt>いっしょ</rt></ruby>に<ruby>夕食<rt>ゆうしょく</rt></ruby>を<ruby>食<rt>た</rt></ruby>べましょう。","dinner","Let's have dinner together.","Noun"],
  ["bánh","Tôi thích bánh.","お<ruby>菓子<rt>かし</rt></ruby> / パン","お<ruby>菓子<rt>かし</rt></ruby>が<ruby>好<rt>す</rt></ruby>きです。","cake/bread","I like cake.","Noun"],
  ["trái cây","Trái cây tươi.","<ruby>果物<rt>くだもの</rt></ruby>","<ruby>新鮮<rt>しんせん</rt></ruby>な<ruby>果物<rt>くだもの</rt></ruby>。","fruit","Fresh fruit.","Noun"],
  ["rau","Ăn nhiều rau.","<ruby>野菜<rt>やさい</rt></ruby>","<ruby>野菜<rt>やさい</rt></ruby>をたくさん<ruby>食<rt>た</rt></ruby>べる。","vegetable","Eat lots of vegetables.","Noun"],
  ["thịt bò","Thịt bò ngon.","<ruby>牛肉<rt>ぎゅうにく</rt></ruby>","<ruby>牛肉<rt>ぎゅうにく</rt></ruby>は<ruby>美味<rt>おい</rt></ruby>しい。","beef","Beef is delicious.","Noun"],
  ["thịt heo","Thịt heo nướng.","<ruby>豚肉<rt>ぶたにく</rt></ruby>","<ruby>焼<rt>や</rt></ruby>き<ruby>豚<rt>ぶた</rt></ruby>。","pork","Grilled pork.","Noun"],
  ["thịt gà","Thịt gà luộc.","<ruby>鶏肉<rt>とりにく</rt></ruby>","<ruby>茹<rt>ゆ</rt></ruby>で<ruby>鶏肉<rt>とりにく</rt></ruby>。","chicken","Boiled chicken.","Noun"],
  ["cá","Tôi thích ăn cá.","<ruby>魚<rt>さかな</rt></ruby>","<ruby>魚<rt>さかな</rt></ruby>が<ruby>好<rt>す</rt></ruby>きです。","fish","I like fish.","Noun"],
  ["trứng","Trứng chiên.","<ruby>卵<rt>たまご</rt></ruby>","<ruby>目玉焼<rt>めだまや</rt></ruby>き。","egg","Fried egg.","Noun"],
  ["sữa","Một ly sữa.","<ruby>牛乳<rt>ぎゅうにゅう</rt></ruby>","<ruby>牛乳<rt>ぎゅうにゅう</rt></ruby><ruby>一杯<rt>いっぱい</rt></ruby>。","milk","A glass of milk.","Noun"],
  ["nước","Cho tôi nước lọc.","<ruby>水<rt>みず</rt></ruby>","お<ruby>水<rt>みず</rt></ruby>をください。","water","Water please.","Noun"],
  ["nước đá","Cho thêm nước đá.","<ruby>氷<rt>こおり</rt></ruby>","<ruby>氷<rt>こおり</rt></ruby>をもっとください。","ice","More ice please.","Noun"],
  ["đường","Cho ít đường thôi.","<ruby>砂糖<rt>さとう</rt></ruby>","<ruby>砂糖<rt>さとう</rt></ruby>を<ruby>少<rt>すこ</rt></ruby>しだけ。","sugar","Just a little sugar.","Noun"],

  # ── Daily/Household (15) ────────────────────────────────────
  ["chìa khoá","Quên chìa khoá rồi.","<ruby>鍵<rt>かぎ</rt></ruby>","<ruby>鍵<rt>かぎ</rt></ruby>を<ruby>忘<rt>わす</rt></ruby>れました。","key","Forgot the key.","Noun"],
  ["ví","Ví tiền của tôi.","<ruby>財布<rt>さいふ</rt></ruby>","<ruby>私<rt>わたし</rt></ruby>の<ruby>財布<rt>さいふ</rt></ruby>です。","wallet","My wallet.","Noun"],
  ["túi","Để vào túi đi.","<ruby>袋<rt>ふくろ</rt></ruby> / カバン","<ruby>袋<rt>ふくろ</rt></ruby>に<ruby>入<rt>い</rt></ruby>れてください。","bag","Put it in the bag.","Noun"],
  ["balo","Balo nhẹ.","リュック","<ruby>軽<rt>かる</rt></ruby>いリュック。","backpack","Light backpack.","Noun"],
  ["đồng hồ","Đồng hồ đẹp.","<ruby>時計<rt>とけい</rt></ruby>","きれいな<ruby>時計<rt>とけい</rt></ruby>。","watch/clock","Pretty watch.","Noun"],
  ["kính","Tôi cần đeo kính.","<ruby>眼鏡<rt>めがね</rt></ruby>","<ruby>眼鏡<rt>めがね</rt></ruby>が<ruby>必要<rt>ひつよう</rt></ruby>です。","glasses","I need glasses.","Noun"],
  ["dù","Mang dù theo nhé.","<ruby>傘<rt>かさ</rt></ruby>","<ruby>傘<rt>かさ</rt></ruby>を<ruby>持<rt>も</rt></ruby>って<ruby>行<rt>い</rt></ruby>って。","umbrella","Take an umbrella.","Noun"],
  ["nón","Đội nón vào.","<ruby>帽子<rt>ぼうし</rt></ruby>","<ruby>帽子<rt>ぼうし</rt></ruby>をかぶってください。","hat","Put on a hat.","Noun"],
  ["máy giặt","Máy giặt hỏng rồi.","<ruby>洗濯機<rt>せんたくき</rt></ruby>","<ruby>洗濯機<rt>せんたくき</rt></ruby>が<ruby>壊<rt>こわ</rt></ruby>れました。","washing machine","Washer is broken.","Noun"],
  ["tủ lạnh","Để vào tủ lạnh.","<ruby>冷蔵庫<rt>れいぞうこ</rt></ruby>","<ruby>冷蔵庫<rt>れいぞうこ</rt></ruby>に<ruby>入<rt>い</rt></ruby>れてください。","refrigerator","Put in the fridge.","Noun"],
  ["máy lạnh","Bật máy lạnh đi.","エアコン","エアコンをつけてください。","air conditioner","Turn on the AC.","Noun"],
  ["quạt","Bật quạt cho mát.","<ruby>扇風機<rt>せんぷうき</rt></ruby>","<ruby>扇風機<rt>せんぷうき</rt></ruby>をつける。","fan","Turn on the fan.","Noun"],
  ["đèn","Đèn sáng quá.","<ruby>電気<rt>でんき</rt></ruby> / ランプ","<ruby>電気<rt>でんき</rt></ruby>が<ruby>明<rt>あか</rt></ruby>るすぎます。","light","Light is too bright.","Noun"],
  ["thảm","Thảm mềm.","カーペット","カーペットは<ruby>柔<rt>やわ</rt></ruby>らかいです。","carpet","Soft carpet.","Noun"],
  ["sô-pha","Ngồi sô-pha xem TV.","ソファ","ソファに<ruby>座<rt>すわ</rt></ruby>ってテレビを<ruby>見<rt>み</rt></ruby>る。","sofa","Sit on sofa watching TV.","Noun"],
]

# Load existing data
html = HTML.read_text(encoding="utf-8")
m = re.search(r'const D=(\[.*?\]);', html, re.DOTALL)
existing = json.loads(m.group(1))
existing_vn_lower = {c["vn"].lower() for c in existing}
existing_no_max = max(c["no"] for c in existing)

added, skipped = 0, 0
to_add = []
for row in NEW:
    vn, vn_ex, jp, jp_ex, en, en_ex, tag = row
    if vn.lower() in existing_vn_lower:
        skipped += 1
        continue
    existing_no_max += 1
    to_add.append({
        "no": existing_no_max, "cat": "Core Basic", "vn": vn,
        "vn_a": vn_ex, "vn_b": vn_ex,
        "jp": jp, "jp_a": jp_ex, "jp_b": jp_ex,
        "en": en, "en_a": en_ex, "en_b": en_ex,
        "tag": tag,
    })
    existing_vn_lower.add(vn.lower())
    added += 1

merged = existing + to_add
core_count = sum(1 for c in merged if c["cat"] == "Core Basic")
print(f"Added: {added}, Skipped duplicates: {skipped}")
print(f"Core Basic now: {core_count}, Total cards: {len(merged)}")

# Save and inject
Path("data").mkdir(exist_ok=True)
Path("data/word_cards_v2.json").write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")

data_line = "const D=" + json.dumps(merged, ensure_ascii=False) + ";"
new_html = re.sub(r'const D=\[.*?\];', lambda _: data_line, html, count=1, flags=re.DOTALL)
HTML.write_text(new_html, encoding="utf-8")
INDEX.write_text(new_html, encoding="utf-8")
print(f"Injected. New file size: {len(new_html):,} bytes")
