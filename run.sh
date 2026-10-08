#!/bin/bash
# ==========================================
# بوابة تسلا الزمنية - أوامر التشغيل السريع
# ARCHITECT: EssamElkomy369
# ==========================================

cd ~/tesla_web_portal

case "$1" in
    start)
        echo "🚀 تشغيل السيرفر..."
        python app.py
        ;;
    bg)
        echo "🚀 تشغيل السيرفر في الخلفية..."
        nohup python app.py > server.log 2>&1 &
        echo "✅ شغال! الـ log في server.log"
        echo "افتح: http://127.0.0.1:5000"
        ;;
    stop)
        echo "🛑 إيقاف السيرفر..."
        pkill -f "python app.py"
        echo "✅ اتوقف"
        ;;
    restart)
        echo "🔄 إعادة تشغيل..."
        pkill -f "python app.py"
        sleep 1
        nohup python app.py > server.log 2>&1 &
        echo "✅ اشتغل تاني"
        ;;
    log)
        tail -f server.log
        ;;
    backup)
        echo "💾 نسخة احتياطية..."
        cp app.py app.py.bak
        cp templates/index.html templates/index.html.bak
        echo "✅ اتعملت النسخة"
        ;;
    *)
        echo "الاستخدام:"
        echo "  ./run.sh start    - تشغيل عادي"
        echo "  ./run.sh bg       - تشغيل في الخلفية"
        echo "  ./run.sh stop     - إيقاف"
        echo "  ./run.sh restart  - إعادة تشغيل"
        echo "  ./run.sh log      - متابعة الـ log"
        echo "  ./run.sh backup   - نسخة احتياطية"
        ;;
esac
