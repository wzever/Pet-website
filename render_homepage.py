import random
import re
import pymysql
from flask import Flask, request, render_template
app = Flask(__name__)

conn_1 = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='pwz20011121',
        db='test',  
        charset='utf8')

conn = pymysql.connect(
    host='192.168.94.215',
    port=3306,
    user='user',
    passwd='111111',
    charset='utf8',
    db='conservation')
cursor_1 = conn_1.cursor()
cursor = conn.cursor() 

# 首页
@app.route('/',methods=['POST','GET'])
@app.route('/home.html',methods=['POST','GET'])
@app.route('/home',methods=['POST','GET'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        userInput = request.form.get('userinput')
        cursor_1.execute(f'SELECT * FROM pet_data WHERE 中文名 LIKE "%{userInput}%"')
        result = cursor_1.fetchall()
        # print(result)
        size = len(result)
        imglist = [result[i][-1].replace('[','').replace(']','').replace('\'','').split(', ')[0] for i in range(size)]
        namelist = [result[i][1] for i in range(size)]
        introlist = [result[i][-2][:70]+'...' for i in range(size)]
        idlist = [result[i][0] for i in range(size)]
        return render_template('search_result.html',size=size,imgs=imglist,names=namelist,intros=introlist,ids=idlist)

# all data
cursor_1.execute('SELECT * FROM pet_data WHERE 宠物类别 = "犬"')
dogs = cursor_1.fetchall()
cursor_1.execute('SELECT * FROM pet_data WHERE 宠物类别 = "猫"')
cats = cursor_1.fetchall()
cursor_1.execute('SELECT * FROM pet_data WHERE 宠物类别 != "猫" and 宠物类别 != "犬"')
others = list(cursor_1.fetchall())
last = ('--' for i in range(34))
others.append(tuple(last))

# 犬类大全
@app.route('/dog.html',methods=['POST','GET'])
@app.route('/dog',methods=['POST','GET'])
def all_dogs():
    if request.method == 'POST':
        userInput = request.form.get('page')
        if userInput.isdigit():
            page = int(userInput)
            imglist = [dogs[i][-1].replace('[','').replace(']','').replace('\'','').split(', ')[0] for i in range(12*(page-1),12*page)]
            namelist = [dogs[i][1] for i in range(12*(page-1),12*page)]
            introlist = [dogs[i][-2][:70]+'...' for i in range(12*(page-1),12*page)]
            idlist = [dogs[i][0] for i in range(12*(page-1),12*page)]
            return render_template('dog.html',imgs=imglist,names=namelist,intros=introlist,page=page,ids=idlist)
        else:
            cursor_1.execute(f'SELECT * FROM pet_data WHERE 中文名 LIKE "%{userInput}%"')
            result = cursor_1.fetchall()
            size = len(result)
            imglist = [result[i][-1].replace('[','').replace(']','').replace('\'','').split(', ')[0] for i in range(size)]
            namelist = [result[i][1] for i in range(size)]
            introlist = [result[i][-2][:70]+'...' for i in range(size)]
            idlist = [result[i][0] for i in range(size)]
            return render_template('search_result.html',size=size,imgs=imglist,names=namelist,intros=introlist,ids=idlist)

    else:
        if not request.args.get('page'):
            page = 1
        else:
            page = int(request.args.get('page'))
        imglist = [dogs[i][-1].replace('[','').replace(']','').replace('\'','').split(', ')[0] for i in range(12*(page-1),12*page)]
        namelist = [dogs[i][1] for i in range(12*(page-1),12*page)]
        introlist = [dogs[i][-2][:70]+'...' for i in range(12*(page-1),12*page)]
        idlist = [dogs[i][0] for i in range(12*(page-1),12*page)]
        return render_template('dog.html',imgs=imglist,names=namelist,intros=introlist,page=page,ids=idlist)

# 猫类大全
@app.route('/cat.html',methods=['POST','GET'])
@app.route('/cat',methods=['POST','GET'])
def all_cats():
    if request.method == 'POST':
        userInput = request.form.get('page')
        if userInput.isdigit():
            page = int(userInput)
            imglist = [cats[i][-1].replace('[','').replace(']','').replace('\'','').split(', ')[0] for i in range(12*(page-1),9*page)]
            namelist = [cats[i][1] for i in range(12*(page-1),12*page)]
            introlist = [cats[i][-2][:70]+'...' for i in range(12*(page-1),12*page)]
            idlist = [cats[i][0] for i in range(12*(page-1),12*page)]
            return render_template('cat.html',imgs=imglist,names=namelist,intros=introlist,page=page,ids=idlist)
        else:
            cursor_1.execute(f'SELECT * FROM pet_data WHERE 中文名 LIKE "%{userInput}%"')
            result = cursor_1.fetchall()
            size = len(result)
            imglist = [result[i][-1].replace('[','').replace(']','').replace('\'','').split(', ')[0] for i in range(size)]
            namelist = [result[i][1] for i in range(size)]
            introlist = [result[i][-2][:70]+'...' for i in range(size)]
            idlist = [result[i][0] for i in range(size)]
            return render_template('search_result.html',size=size,imgs=imglist,names=namelist,intros=introlist,ids=idlist)

    else:
        if not request.args.get('page'):
            page = 1
        else:
            page = int(request.args.get('page'))
        imglist = [cats[i][-1].replace('[','').replace(']','').replace('\'','').split(', ')[0] for i in range(12*(page-1),12*page)]
        namelist = [cats[i][1] for i in range(12*(page-1),12*page)]
        introlist = [cats[i][-2][:70]+'...' for i in range(12*(page-1),12*page)]
        idlist = [cats[i][0] for i in range(12*(page-1),12*page)]
        return render_template('cat.html',imgs=imglist,names=namelist,intros=introlist,page=page,ids=idlist)

# 其他类大全
@app.route('/other.html',methods=['POST','GET'])
@app.route('/other',methods=['POST','GET'])
def all_others():
    if request.method == 'POST':
        userInput = request.form.get('page')
        if userInput.isdigit():
            page = int(userInput)
            imglist = [others[i][-1].replace('[','').replace(']','').replace('\'','').split(', ')[0] for i in range(12*(page-1),9*page)]
            namelist = [others[i][1] for i in range(12*(page-1),12*page)]
            introlist = [others[i][-5][:70]+'...' for i in range(12*(page-1),12*page)]
            idlist = [others[i][0] for i in range(12*(page-1),12*page)]
            return render_template('other.html',imgs=imglist,names=namelist,intros=introlist,page=page,ids=idlist)
        else:
            cursor_1.execute(f'SELECT * FROM pet_data WHERE 中文名 LIKE "%{userInput}%"')
            result = cursor_1.fetchall()
            size = len(result)
            imglist = [result[i][-1].replace('[','').replace(']','').replace('\'','').split(', ')[0] for i in range(size)]
            namelist = [result[i][1] for i in range(size)]
            introlist = [result[i][-5][:70]+'...' for i in range(size)]
            idlist = [result[i][0] for i in range(size)]
            return render_template('search_result.html',size=size,imgs=imglist,names=namelist,intros=introlist,ids=idlist)
    else:
        if not request.args.get('page'):
            page = 1
        else:
            page = int(request.args.get('page'))
        imglist = [others[i][-1].replace('[','').replace(']','').replace('\'','').split(', ')[0] for i in range(12*(page-1),12*page)]
        namelist = [others[i][1] for i in range(12*(page-1),12*page)]
        introlist = [others[i][-5][:70]+'...' for i in range(12*(page-1),12*page)]
        idlist = [others[i][0] for i in range(12*(page-1),12*page)]
        return render_template('other.html',imgs=imglist,names=namelist,intros=introlist,page=page,ids=idlist)

# 详情
@app.route('/detail',methods=['POST','GET'])
def dog_details():
    randids = [random.randint(0,380) for i in range(6)]
    adv = []
    for rand_id in randids:
        cursor_1.execute(f'SELECT * FROM pet_data WHERE id = {rand_id}')
        adv.append(cursor_1.fetchall()[0])
    rcimgs = [adv[i][-1].replace('[','').replace(']','').replace('\'','').split(', ')[0] for i in range(6)]
    if not request.args.get('id'):    
        id = 0
    else:
        id = int(request.args.get('id'))
    # print(id)
    cursor_1.execute(f'SELECT * FROM pet_data WHERE ID = "{id}"')
    info = cursor_1.fetchall()[0]
    img = info[-1].replace('[','').replace(']','').replace('\'','').split(', ')[-1]
    # print(info)
    return render_template('detail.html',info=info,img=img,adv=adv,rcimgs=rcimgs)

# 数据可视
@app.route('/map-polygon.html',methods=['GET'])
@app.route('/map-polygon',methods=['GET'])
def map():
    return render_template('map-polygon.html')

@app.route('/map2.html',methods=['GET'])
@app.route('/map2',methods=['GET'])
def map2():
    return render_template('visual2.html')

# 关于我们
@app.route('/about.html',methods=['GET'])
@app.route('/about',methods=['GET'])
def about():
    return render_template('about_this_web.html')

@app.route('/members.html',methods=['GET'])
@app.route('/members',methods=['GET'])
def members():
    return render_template('member_introduction.html')

# 宠物服务
@app.route('/service.html',methods=['GET'])
@app.route('/service',methods=['GET'])
def service():
    return render_template('service.html')

'''hospital'''
@app.route('/service1.html',methods=['GET','POST'])
@app.route('/service1',methods=['GET','POST'])
def service1():
    if request.method=='POST':
        page=request.form.get('page')
        lenght=len(page)
        try:
            low=(int(page)-1)*9
            high=(int(page)*9)
            cursor.execute('SELECT * FROM hospital WHERE id>{} and id<={}'.format(low,high))
            result=cursor.fetchall()
            
            lenth=len(result)
            conn.commit()
            data=[{} for m0 in range(lenth)]
            for i in range(lenth):
                dis=result[i][1][:35]+'···'
                data[i]['title']=result[i][0]
                data[i]['dis']=dis
                data[i]['img']=result[i][2]
                data[i]['id']=result[i][3]
            if int(page)>1 and int(page)<30:
                page1=int(page)-1
                page2=int(page)+1
            elif int(page)<=1:
                page1=1
                page2=2
            else:
                page1=29
                page2=30
        except:
            page='"%'+page+'%"'
            cursor.execute('SELECT * FROM hospital WHERE title LIKE  {}'.format(page))
            result=cursor.fetchall()
            conn.commit()
            
            lenth=len(result)
            data=[{} for m1 in range(lenth)]
            for i in range(lenth):
                dis=result[i][1][:35]+'···'
                data[i]['title']=result[i][0]
                data[i]['dis']=dis
                data[i]['img']=result[i][2]
                data[i]['id']=result[i][3]
            page1=1
            page2=2
            
    else:
        try :
            page=request.args.get('page')    
            low=(int(page)-1)*9
            high=(int(page)*9)
            cursor.execute('SELECT * FROM hospital WHERE id>{} and id<={}'.format(low,high))
            result=cursor.fetchall()
            conn.commit()
            data=[{} for m2 in range(9)]
            for i in range(9):
                dis=result[i][1][:35]+'···'
                data[i]['title']=result[i][0]
                data[i]['dis']=dis
                data[i]['img']=result[i][2]
                data[i]['id']=result[i][3]
            if int(page)>1 and int(page)<30:
                page1=int(page)-1
                page2=int(page)+1
            elif int(page)<=1:
                page1=1
                page2=2
            else:
                page1=29
                page2=30
        except:    
            page='1'
            low=(int(page)-1)*9
            high=(int(page)*9)
            cursor.execute('SELECT * FROM hospital WHERE id>{} and id<={}'.format(low,high))
            result=cursor.fetchall()
            conn.commit()
            data=[{} for m2 in range(9)]
            for i in range(9):
                dis=result[i][1][:35]+'···'
                data[i]['title']=result[i][0]
                data[i]['dis']=dis
                data[i]['img']=result[i][2]
                data[i]['id']=result[i][3]
            page1=1
            page2=2
    return render_template('service1.html',data=data,page1=page1,page2=page2)
'''conservation'''
@app.route('/service2.html',methods=['GET','POST'])
@app.route('/service2',methods=['GET','POST'])
def service2():
    if request.method=='POST':
        page=request.form.get('page')
        lenght=len(page)
        try :
            low=(int(page)-1)*9
            high=(int(page)*9)
            cursor.execute('SELECT * FROM conservation WHERE id>{} and id<={}'.format(low,high))
            result=cursor.fetchall()
            
            lenth=len(result)
            conn.commit()
            data=[{} for m0 in range(lenth)]
            for i in range(lenth):
                dis=result[i][1][:35]+'···'
                data[i]['title']=result[i][0]
                data[i]['dis']=dis
                data[i]['img']=result[i][2]
                data[i]['id']=result[i][3]
            if int(page)>1 and int(page)<30:
                page1=int(page)-1
                page2=int(page)+1
            elif int(page)<=1:
                page1=1
                page2=2
            else:
                page1=29
                page2=30
        except:
            page='"%'+page+'%"'
            cursor.execute('SELECT * FROM conservation WHERE title LIKE  {}'.format(page))
            result=cursor.fetchall()
            conn.commit()
            
            lenth=len(result)
            data=[{} for m1 in range(lenth)]
            for i in range(lenth):
                dis=result[i][1][:35]+'···'
                data[i]['title']=result[i][0]
                data[i]['dis']=dis
                data[i]['img']=result[i][2]
                data[i]['id']=result[i][3]
            page1=1
            page2=2
            
    else:
        try :
            page=request.args.get('page')    
            low=(int(page)-1)*9
            high=(int(page)*9)
            cursor.execute('SELECT * FROM conservation WHERE id>{} and id<={}'.format(low,high))
            result=cursor.fetchall()
            conn.commit()
            data=[{} for m2 in range(9)]
            for i in range(9):
                dis=result[i][1][:35]+'···'
                data[i]['title']=result[i][0]
                data[i]['dis']=dis
                data[i]['img']=result[i][2]
                data[i]['id']=result[i][3]
            if int(page)>1 and int(page)<30:
                page1=int(page)-1
                page2=int(page)+1
            elif int(page)<=1:
                page1=1
                page2=2
            else:
                page1=29
                page2=30
        except:    
            page='1'
            low=(int(page)-1)*9
            high=(int(page)*9)
            cursor.execute('SELECT * FROM conservation WHERE id>{} and id<={}'.format(low,high))
            result=cursor.fetchall()
            conn.commit()
            data=[{} for m2 in range(9)]
            for i in range(9):
                dis=result[i][1][:35]+'···'
                data[i]['title']=result[i][0]
                data[i]['dis']=dis
                data[i]['img']=result[i][2]
                data[i]['id']=result[i][3]
            page1=1
            page2=2
    return render_template('service2.html',data=data,page1=page1,page2=page2)
'''train'''
@app.route('/service3.html',methods=['GET','POST'])
@app.route('/service3',methods=['GET','POST'])
def service3():
    if request.method=='POST':
        page=request.form.get('page')
        lenght=len(page)
        try :
            low=(int(page)-1)*9
            high=(int(page)*9)
            cursor.execute('SELECT * FROM train WHERE id>{} and id<={}'.format(low,high))
            result=cursor.fetchall()
            
            lenth=len(result)
            conn.commit()
            data=[{} for m0 in range(lenth)]
            for i in range(lenth):
                dis=result[i][1][:35]+'···'
                data[i]['title']=result[i][0]
                data[i]['dis']=dis
                data[i]['img']=result[i][2]
                data[i]['id']=result[i][3]
            if int(page)>1 and int(page)<30:
                page1=int(page)-1
                page2=int(page)+1
            elif int(page)<=1:
                page1=1
                page2=2
            else:
                page1=29
                page2=30
        except:
            page='"%'+page+'%"'
            cursor.execute('SELECT * FROM train WHERE title LIKE  {}'.format(page))
            result=cursor.fetchall()
            conn.commit()
            
            lenth=len(result)
            data=[{} for m1 in range(lenth)]
            for i in range(lenth):
                dis=result[i][1][:35]+'···'
                data[i]['title']=result[i][0]
                data[i]['dis']=dis
                data[i]['img']=result[i][2]
                data[i]['id']=result[i][3]
            page1=1
            page2=2
    else:
        try :
            page=request.args.get('page')    
            low=(int(page)-1)*9
            high=(int(page)*9)
            cursor.execute('SELECT * FROM train WHERE id>{} and id<={}'.format(low,high))
            result=cursor.fetchall()
            conn.commit()
            data=[{} for m2 in range(9)]
            for i in range(9):
                dis=result[i][1][:35]+'···'
                data[i]['title']=result[i][0]
                data[i]['dis']=dis
                data[i]['img']=result[i][2]
                data[i]['id']=result[i][3]
            if int(page)>1 and int(page)<30:
                page1=int(page)-1
                page2=int(page)+1
            elif int(page)<=1:
                page1=1
                page2=2
            else:
                page1=29
                page2=30
        except:    
            page='1'
            low=(int(page)-1)*9
            high=(int(page)*9)
            cursor.execute('SELECT * FROM train WHERE id>{} and id<={}'.format(low,high))
            result=cursor.fetchall()
            conn.commit()
            data=[{} for m2 in range(9)]
            for i in range(9):
                dis=result[i][1][:35]+'···'
                data[i]['title']=result[i][0]
                data[i]['dis']=dis
                data[i]['img']=result[i][2]
                data[i]['id']=result[i][3]
            page1=1
            page2=2
    return render_template('service3.html',data=data,page1=page1,page2=page2)
'''fun'''
@app.route('/service4.html',methods=['GET','POST'])
@app.route('/service4',methods=['GET','POST'])
def service4():
    if request.method=='POST':
        page=request.form.get('page')
        lenght=len(page)
        try :
            low=(int(page)-1)*9
            high=(int(page)*9)
            cursor.execute('SELECT * FROM fun WHERE id>{} and id<={}'.format(low,high))
            result=cursor.fetchall()
            
            lenth=len(result)
            conn.commit()
            data=[{} for m0 in range(lenth)]
            for i in range(lenth):
                dis=result[i][1][:35]+'···'
                data[i]['title']=result[i][0]
                data[i]['dis']=dis
                data[i]['img']=result[i][2]
                data[i]['id']=result[i][3]
            if int(page)>1 and int(page)<30:
                page1=int(page)-1
                page2=int(page)+1
            elif int(page)<=1:
                page1=1
                page2=2
            else:
                page1=29
                page2=30
        except:
            page='"%'+page+'%"'
            cursor.execute('SELECT * FROM fun WHERE title LIKE  {}'.format(page))
            result=cursor.fetchall()
            conn.commit()
            
            lenth=len(result)
            data=[{} for m1 in range(lenth)]
            for i in range(lenth):
                dis=result[i][1][:35]+'···'
                data[i]['title']=result[i][0]
                data[i]['dis']=dis
                data[i]['img']=result[i][2]
                data[i]['id']=result[i][3]
            page1=1
            page2=2    
    else:
        try :
            page=request.args.get('page')    
            low=(int(page)-1)*9
            high=(int(page)*9)
            cursor.execute('SELECT * FROM fun WHERE id>{} and id<={}'.format(low,high))
            result=cursor.fetchall()
            conn.commit()
            data=[{} for m2 in range(9)]
            for i in range(9):
                dis=result[i][1][:35]+'···'
                data[i]['title']=result[i][0]
                data[i]['dis']=dis
                data[i]['img']=result[i][2]
                data[i]['id']=result[i][3]
            if int(page)>1 and int(page)<30:
                page1=int(page)-1
                page2=int(page)+1
            elif int(page)<=1:
                page1=1
                page2=2
            else:
                page1=29
                page2=30
        except:    
            page='1'
            low=(int(page)-1)*9
            high=(int(page)*9)
            cursor.execute('SELECT * FROM fun WHERE id>{} and id<={}'.format(low,high))
            result=cursor.fetchall()
            conn.commit()
            data=[{} for m2 in range(9)]
            for i in range(9):
                dis=result[i][1][:35]+'···'
                data[i]['title']=result[i][0]
                data[i]['dis']=dis
                data[i]['img']=result[i][2]
                data[i]['id']=result[i][3]
            page1=1
            page2=2
    return render_template('service4.html',data=data,page1=page1,page2=page2)
@app.route('/service-details.html',methods=['post','GET'])
@app.route('/service-details',methods=['post','GET'])
def servicedetails():
    request_method=request.method
    data=('','','')
    id=request.args.get('id')
    id=int(id)
    name=request.args.get('name')
    name=int(name)
    if name==1:
        cursor.execute('SELECT * FROM hospital WHERE id={}'.format(id))
        data=cursor.fetchone()
        cursor.execute('SELECT * FROM hospital WHERE id >= ((SELECT MAX(id) FROM hospital)-(SELECT MIN(id) FROM hospital)) * RAND() + (SELECT MIN(id) FROM hospital)  LIMIT 6')
        otherdata=cursor.fetchall()
        conn.commit()
        return  render_template('/service-details.html',data=data,name=name,otherdata=otherdata)
    elif name==2:
        cursor.execute('SELECT * FROM conservation WHERE id={}'.format(id))
        data=cursor.fetchone()
        cursor.execute('SELECT * FROM conservation WHERE id >= ((SELECT MAX(id) FROM conservation)-(SELECT MIN(id) FROM conservation)) * RAND() + (SELECT MIN(id) FROM conservation)  LIMIT 6')
        otherdata=cursor.fetchall()
        conn.commit()
        return  render_template('/service-details.html',data=data,name=name,otherdata=otherdata)
    elif name==3:
        cursor.execute('SELECT * FROM train WHERE id={}'.format(id))
        data=cursor.fetchone()
        cursor.execute('SELECT * FROM train WHERE id >= ((SELECT MAX(id) FROM train)-(SELECT MIN(id) FROM train)) * RAND() + (SELECT MIN(id) FROM train)  LIMIT 6')
        otherdata=cursor.fetchall()
        conn.commit()
        return  render_template('/service-details.html',data=data,name=name,otherdata=otherdata)
    elif name==4:
        cursor.execute('SELECT * FROM fun WHERE id={}'.format(id))
        data=cursor.fetchone()
        cursor.execute('SELECT * FROM fun WHERE id >= ((SELECT MAX(id) FROM fun)-(SELECT MIN(id) FROM fun)) * RAND() + (SELECT MIN(id) FROM fun)  LIMIT 6')
        otherdata=cursor.fetchall()
        conn.commit()
        return  render_template('/service-details.html',data=data,name=name,otherdata=otherdata)
    return  render_template('/service-details.html',data=data)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)