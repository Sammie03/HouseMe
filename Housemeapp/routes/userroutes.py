import math, random, os, re
from flask import render_template, request, abort, redirect, flash, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash

from Housemeapp import app,db, Message, mail
from Housemeapp.mymodels import Amenities, Property_owner, Property_type, User, States, Lga, Property, Property_amenities, Property_images
# from Housemeapp.forms import LoginForm


@app.route('/')
def homepage():
            states = db.session.query(States).all()
            lga = db.session.query(Lga).all()
            property = db.session.query(Property_type).all()
            properties = db.session.query(Property).order_by(Property.date_posted.desc()).limit(3)
            
            return render_template("user/index.html", states=states, property=property, properties=properties, lga=lga)
        


         
@app.route('/index/searchbox/', methods=['POST'])
def searchbox():
    
            states = db.session.query(States).all()
            property = db.session.query(Property_type).all()
            properties = db.session.query(Property).order_by(Property.date_posted.desc())

            keyword = request.form.get('keywords')
            state = request.form.get('state')
            lgachoice = request.form.get('lga')
            proptype = request.form.get('proptype')
            minprice = request.form.get('minprice')
            maxprice = request.form.get('maxprice')
            
            keywordsearch = "%{}%".format(keyword)
            
            filterstr =""
                
            if proptype !="":
                 filterstr= filterstr + (Property.property_typeid==proptype)   
                 
            if keyword !="":
                filterstr= filterstr + (Property.property_address.like(keywordsearch))
                      
            if state !="":
                 filterstr= filterstr + (States.state_id==state)
                             
            if lgachoice !="":
                 filterstr= filterstr + (Lga.lga_id==lgachoice)
                 
            if minprice !="":
                 filterstr= filterstr + (Property.property_price==minprice)
                
            properties = db.session.query(Property).filter(filterstr).all()   
                
                 
            return render_template("user/property.html", properties=properties, property=property, states=states)
        

           


@app.route('/about/us/')
def aboutus():
    return render_template("user/aboutus.html")



@app.route('/contact/us/')
def contactus():
    return render_template("user/contactus.html")



@app.route('/user/login/')
def userlogin():
    return render_template('user/login.html')


@app.route('/user/login/validation', methods=['GET','POST'])
def validatelogin():
        useremail = request.form.get('useremail')
        password = request.form.get('userpwd')
            
        if useremail=='' or password=='':
                flash('Please ensure all fields are filled')
                return redirect('/user/login')
        else:
            userdetails = db.session.query(User).filter(User.user_email==useremail).first()
            if userdetails:
                formatted_password = userdetails.user_pword
                check= check_password_hash(formatted_password,password)
                if check:
                    session['loggedin'] = userdetails.user_id
                    return render_template("user/userdashboard.html", userdetails=userdetails)
                else:
                    flash("Invalid login credentials")
                    return redirect('/user/login')
            else:
                flash("Please reconfirm details")
                return redirect('/user/login')
            
            
    
        
@app.route('/user/logout')
def userlogout():
    session.pop('loggedin')
    return redirect('/user/login/')
       
                
                

@app.route('/property/owner/login/', methods=['GET','POST'])
def pownerlogin():
    return render_template("user/pownerlogin.html")




@app.route('/powner/login/validation', methods=['GET','POST'])
def validatepownerlogin():
        powneremail = request.form.get('powneremail')
        password = request.form.get('pownerpwd')
            
        if powneremail=='' or password=='':
                flash('please ensure all fields are filled')
                return redirect('/property/owner/login/')
        else:
            pownerdetails = db.session.query(Property_owner).filter(Property_owner.owner_email==powneremail).first()
            properties = db.session.query(Property).order_by(Property.date_posted.desc())
            if pownerdetails:
                formatted_password = pownerdetails.owner_pword
                check= check_password_hash(formatted_password,password)
                if check:
                    session['ownerloggedin'] = pownerdetails.owner_id
                    return render_template("user/propertyowner.html", pownerdetails=pownerdetails, properties=properties)
                else:
                    flash("Invalid login credentials")
                    return redirect('/property/owner/login/')
            else:
                flash("Please reconfirm details")
                return redirect('/property/owner/login/')
            
            
            

@app.route('/owner/profile')
def pownerprofile():
        ownerloggedin = session.get('ownerloggedin')
        if ownerloggedin == None:
            return redirect('/property/owner/login/')
        else:
            propertyowner = db.session.query(Property_owner).get(ownerloggedin)
            return render_template('user/ownerprofile.html', propertyowner=propertyowner)
        
        
        
        
@app.route('/user/profile')
def userprofile():
      userlogged = session.get('loggedin')
      if userlogged ==None:
        return redirect('/user/login/')
   
      else:
          user = db.session.query(User).get(userlogged)
          return render_template('user/userprofile.html', user=user)
      
      
      
@app.route("/user/update", methods=['POST','GET'])
def user_update(): 
          userlogged = session.get('loggedin')
          if userlogged ==None:
            return redirect('/user/login/')
          else:
               user = db.session.query(User).get(userlogged)
               
               user.user_fname = request.form.get('userfname')
               user.user_lname = request.form.get('userlname')
               user.user_phone = request.form.get('userphone')
               user.user_email = request.form.get('useremail')
               user.user_username = request.form.get('username')
               user.user_pword = request.form.get('userpw') 
    
               db.session.commit()
               flash("Details updated successfully")
               return redirect('/user/profile')
            
         
         
            
@app.route("/owner/update", methods=['POST','GET'])
def owner_update(): 
        ownerloggedin = session.get('ownerloggedin')
        if ownerloggedin == None:
            return redirect('/property/owner/login/')
        if request.method =='GET':
            return redirect('/property/owner/login/')
        
        else:
            propertyowner = db.session.query(Property_owner).get(ownerloggedin)
        
            propertyowner.owner_fname = request.form.get('pownerfname')
            propertyowner.owner_lname = request.form.get('pownerlname')
            propertyowner.owner_phone = request.form.get('pownerphone')
            propertyowner.owner_email = request.form.get('powneremail')
            propertyowner.owner_username = request.form.get('pownerusername')
            propertyowner.owner_pword = request.form.get('pownerpw')   
        
            db.session.commit()
            flash("Details updated successfully")
            return redirect('/owner/profile')
    
    
    
@app.route('/property/details/update/<id>')
def property_update(id):
    ownerloggedin = session.get('ownerloggedin')
    if ownerloggedin == None:
        return redirect('/property/owner/login/')
    else:
        property = db.session.query(Property).get(id)
        states = db.session.query(States).all()
        lga = db.session.query(Lga).all()
        propertytype = db.session.query(Property_type).all()
        amenities = db.session.query(Amenities).all()
    return render_template('user/propertyupdate.html', property=property, states=states, lga=lga, propertytype=propertytype, amenities=amenities)
    
    
    

@app.route("/owner/property/update/<id>", methods=['POST','GET'])
def owner_property_update(id): 
         ownerloggedin = session.get('ownerloggedin')
         if ownerloggedin == None:
             return redirect('/property/owner/login/')
         else:
             property = db.session.query(Property).get(id)
    
             propertytype = request.form.get('propertytype')
             price = request.form.get('price')
             address = request.form.get('address')
             state = request.form.get('state')
             lga = request.form.get('lga')
             amenities = request.form.getlist('amenities')
             description = request.form.get('description')
             propertyimages = request.files.get('images')
        
             if propertytype =='' or price =='' or address =='' or state =='' or lga =='':
                   flash("Please ensure all fields are filled")
                   return redirect('/post/property/')
               
             else: 
                  
                 db.session.commit()
                 flash("Property details updated successfully")
                 return redirect('/owner/listings')

         


@app.route('/owner/delete/listing/<id>')
def owner_delete(id):
    Owner = session.get('ownerloggedin')
    if Owner ==None:
        return redirect('/property/owner/login/')
    else:
          b = db.session.query(Property).get(id)
          db.session.delete(b)
          db.session.commit()
          flash(f"The property located at {b.property_address} has been successfully deleted")
          return redirect('/owner/listings')
    
    
    
@app.route("/owner/listings")
def owner_listings():
    ownerloggedin = session.get('ownerloggedin')
    if ownerloggedin == None:
            return redirect('/property/owner/login/')
    else:
        ownerproperties = db.session.query(Property).filter(Property.property_ownerid==ownerloggedin)
        return render_template("user/ownerlistings.html", ownerproperties=ownerproperties )
    
                
       
        
@app.route('/property/owner/logout')
def pownerlogout():
    session.pop('ownerloggedin')
    return redirect('/property/owner/login/')


@app.errorhandler(404)
def errorpage(Error):
    return render_template("user/error404.html"),404




@app.route('/list/property/', methods=['GET','POST'])
def listproperty():
        ownerloggedin = session.get('ownerloggedin')
        if ownerloggedin == None:
            return redirect('/property/owner/login/')
        else:
            states = db.session.query(States).all()
            property = db.session.query(Property_type).all()
            lga = db.session.query(Lga).all()
            amenities = db.session.query(Amenities).all()
            return render_template('user/listproperty.html', states=states, property=property,lga=lga, amenities=amenities, property_ownerid=ownerloggedin)
      

    

@app.route('/post/property/', methods=['GET','POST'])
def postproperty():
        ownerloggedin = session.get('ownerloggedin')
        if ownerloggedin == None:
            return redirect('/property/owner/login/')
        else:
            states = db.session.query(States).all()
            property = db.session.query(Property_type).all()
            lga = db.session.query(Lga).all()
            amenities = db.session.query(Amenities).all()
            return render_template('user/postproperty.html', states=states, property=property,lga=lga, amenities=amenities, property_ownerid=ownerloggedin)
    
   
    
    
@app.route('/all/property/details/<id>')
def allpropertydetails(id):
    states = db.session.query(States).all()
    properties = db.session.query(Property_type).all()
    property = db.session.query(Property).filter(Property.property_id == id)
    similarproperty = db.session.query(Property).all()
    return render_template('user/viewproperty.html', property=property, properties=properties, states=states, similarproperty=similarproperty)
      
      
      
@app.route('/property/details', methods=['POST'])
def propertydetails():
    
    ownerloggedin = session.get('ownerloggedin')
    if ownerloggedin == None:
            return redirect('/property/owner/login/')
    else:
        propertytype = request.form.get('propertytype')
        price = request.form.get('price')
        address = request.form.get('address')
        state = request.form.get('state')
        lga = request.form.get('lga')
        amenities = request.form.getlist('amenities')
        description = request.form.get('description')
        propertyimages = request.files.get('images')
        
        powner = Property_owner.query.get(ownerloggedin)
        
        original_file =  propertyimages.filename
        if propertytype =='' or price =='' or address =='' or state =='' or lga =='':
            flash("Please ensure all fields are filled")
            return redirect('/post/property/')
        if original_file !='': 
             extension = os.path.splitext(original_file)
             if extension[1].lower() in ['.jpg','.png', '.jpeg', '.gif', '.tiff', '.raw', '.pdf']:
                 fn = math.ceil(random.random() * 10000000000)  
                 save_as = str(fn)+extension[1] 
                 propertyimages.save(f"Housemeapp/static/images/property_images/{save_as}")
                 
                    
                 p = Property(property_price=price, property_description=description, property_typeid=propertytype, property_address=address, property_lgaid=lga, property_images=save_as, property_ownerid=ownerloggedin)
                 db.session.add(p)
                 db.session.commit()   
                 
                 propid = db.session.query(Property).filter(Property.property_ownerid == ownerloggedin).first()
                 
                 for a in amenities:
                     q = Property_amenities(property_id=propid.property_id, amenities_id=a)
                     db.session.add(q)
                 db.session.commit()
                 
                 flash('Property listed successfully')
                 return redirect('/owner/listings')     
                
             else:
                flash('Image type not allowed')
                return redirect('/post/property/')
        



@app.route('/property/')
def property():
    states = db.session.query(States).all()
    property = db.session.query(Property_type).all()
    properties = db.session.query(Property).order_by(Property.date_posted.desc())
  

    return render_template("user/property.html", property=property, properties=properties,states=states)




@app.route('/property/owner/dashboard/')
def propertyowner():
          ownerloggedin = session.get('ownerloggedin')
          if ownerloggedin == None:
            return redirect('/property/owner/login/')
          else:
               pownerdetails = db.session.query(Property_owner).get(ownerloggedin)
               properties = db.session.query(Property).filter(Property.property_ownerid==ownerloggedin).all()
                           
          return render_template("user/propertyowner.html", pownerdetails=pownerdetails, properties=properties)
    
    
    
    
@app.route('/sort/lga', methods=['POST','GET'])
def sort_lga():
    state = request.form.get('stateid')
    results = db.session.query(Lga).filter(Lga.state_id==state).all()
  
    select_html = "<select>"
    for r in results:
        select_html = select_html + f"<option value={r.lga_id}>{r.lga_name}</option>"
    select_html = select_html + "</select>"

    return select_html
  
   

@app.route('/password/reset/')
def passwordreset():
    return render_template("user/pwreset.html")



@app.route('/sign/up/', methods=['GET','POST'])
def usersignup():

    if request.method == 'GET':
        return render_template("user/signuppage.html")
    else:
        userfname = request.form.get('userfname')
        userlname = request.form.get('userlname')
        useremail = request.form.get('useremail')
        username = request.form.get('username')
        userphone = request.form.get('userphone')
        userpword = request.form.get('userpw')
        confirmuserpword = request.form.get('confirmuserpw')

        userfname = userfname
        userlname = userlname
        userpword = userpword

        namereg = "([0-9])"
        namereg2 = "([a-zA-Z])"
        pwordreg = "^((?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]))"


        if re.search(namereg,userfname) or re.search(namereg,userlname):
            flash("Please ensure First name and Last name doesn't contain digits.")
            return redirect('/sign/up/')
        
        if re.search(namereg2,userfname) == None or re.search(namereg2,userlname) == None:
            flash("Please ensure First name and Last name are valid.")
            return redirect('/sign/up/')

        if re.match(pwordreg,userpword) == None:
            flash("Please ensure password includes atleast one digit, one uppercase and one lowercase letters")
            return redirect('/sign/up/')
        
        if userfname == "" or userlname =="" or useremail =="" or username =="" or userphone =="" or userpword =="":
             flash("Please ensure all fields are filled accurately") 
             return redirect('/sign/up/')

        elif userpword != confirmuserpword:
            flash('Please ensure the passwords match')
            return redirect ('/sign/up/')

        else:
            encryptedpw = generate_password_hash(userpword)
            u = User(user_email=useremail, username=username, user_fname=userfname, user_lname=userlname, user_phone=userphone, user_pword=encryptedpw)
            db.session.add(u)
            db.session.commit()
            id = u.user_id
            session['loggedin'] = id 
            flash("Signup successful, please login below.")
            return redirect('/user/login')
    
    
        

@app.route('/propertyowner/sign/up/', methods=['GET','POST'])
def propertyownersignup():
    if request.method == 'GET':
        return render_template("user/pownersignup.html")
    else:
        pownerfname = request.form.get('pownerfname')
        pownerlname = request.form.get('pownerlname')
        powneremail = request.form.get('powneremail')
        pownerusername = request.form.get('pownerusername')
        pownerphone = request.form.get('pownerphone')
        pownerpw = request.form.get('pownerpw')
        confirmpownerpw = request.form.get('confirmpownerpw')

        pownerfname = pownerfname
        pownerlname = pownerlname
        pownerpw = pownerpw

        reg = "([0-9])"
        reg2 = "([a-bA-B])"
        pwordreg = "^((?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]))"

        if re.search(reg,pownerfname) or re.search(reg,pownerlname):
            flash("Please ensure First name and Last name doesn't contain digits.")
            return redirect('/sign/up/')
        
        if re.search(reg2,pownerfname) == None or re.search(reg2,pownerlname) == None:
            flash("Please ensure First name and Last name are valid.")
            return redirect('/sign/up/')

        if re.match(pwordreg,pownerpw) == None:
            flash("Please ensure password includes atleast one digit, one uppercase and one lowercase letters")
            return redirect('/sign/up/')
        
        if pownerfname == "" or pownerlname =="" or powneremail =="" or pownerusername =="" or pownerphone =="" or pownerpw =="":
             flash("Please ensure all fields are filled accurately") 
             return redirect('/sign/up/')
        elif pownerpw != confirmpownerpw:
            flash('Please reconfirm password')
            return redirect ('/sign/up/')
        else:
            encryptedpw = generate_password_hash(pownerpw)
            p = Property_owner(owner_email=powneremail, owner_username=pownerusername, owner_fname=pownerfname, owner_lname=pownerlname, owner_phone=pownerphone, owner_pword=encryptedpw)
            db.session.add(p)
            db.session.commit()
            id = p.owner_id
            session['ownerloggedin'] = id 
            flash("Signup successful, please login below")
            return redirect('/property/owner/login/')
            



@app.route('/user/dashboard/')
def userdashboard():
    userlogged = session.get('loggedin')
    if userlogged ==None:
        return redirect('/user/login/')
    else:
        userdetails = db.session.query(User).get(userlogged)
        return render_template("user/userdashboard.html", userdetails=userdetails)
    


@app.route('/property/<propertyname>')
def viewproperty(propertyname):
    states = db.session.query(States).all()
    property = db.session.query(Property_type).all()
    return render_template('user/viewproperty.html', states=states, property=property)



# @app.route('/forgot/password', methods=["POST","GET"])
# def forgotpassword():
#     if request.method == "GET":
#         return redirect('/user/login/')
#     else:
#         email = request.form.get("forgotpw")

#         if email:
#             retrievedeets = db.session.query(User).filter(User.user_email==email).first

#             if retrievedeets:
#                 retrievepw = "bigsam"
                     

#                 subject = "Automated Email"
#                 sender = ("Samteddy","eventstrolley@gmail.com")
#                 recipient = ["samuelokediya@gmail.com"]
                
#                 #instantiate an object of Message..
#                 try:
#                     msg=Message(subject=subject,sender=sender,recipients=recipient, body="<b>This is your password</b>")
                
#                 #method2
#                     # msg= Message()
#                     # msg.subject=subject
#                     # msg.sender=sender
#                     # msg.body =""
#                     # msg.recipients=recipient
                    
#                     htmlstr = "<h6>How are you Sammie?</h6><p><img src='https://www.google.com/search?q=images&tbm=isch&source=iu&ictx=1&vet=1&fir=LHY-1Uagl8fCxM%252Cl-X2y9oJGN2i-M%252C_%253BtFT2spaQpfBwhM%252CcMRXOd2p22EgNM%252C_%253B-Iap6zp20DK6KM%252Cl-X2y9oJGN2i-M%252C_%253Ba4JmwRU0zcHUtM%252CISkb2KM1Sl3SmM%252C_%253BkGZWolysFFKPOM%252CM_GLqoPzx6T9DM%252C_%253B2nDXavJs9DoKTM%252CB51x0PBR9KNzvM%252C_%253BWu_WLS_uDRWvOM%252CcMRXOd2p22EgNM%252C_%253BDH7p1w2o_fIU8M%252CBa_eiczVaD9-zM%252C_%253BUpvqeWupXuaMrM%252CISkb2KM1Sl3SmM%252C_%253Bn5hAWsQ-sgKo_M%252C-UStXW0dQEx4SM%252C_%253BsPwUW2x5Z3mupM%252CnBiD9BWYMB87aM%252C_%253BUVAHTXdge9JbrM%252CtnVTsEa64LdCyM%252C_%253BzAGiSuQh5zpsUM%252CtOfiwT7ULtBHIM%252C_%253BD7PWmTEZbduE6M%252C7aaqRtckvukvLM%252C_&usg=AI4_-kS0pZ2iM0yXeFy5Xao-cp2U4n3uYw&sa=X&ved=2ahUKEwj4uKfY1oH3AhVux4UKHUKbASAQ9QF6BAgDEAE#imgrc=LHY-1Uagl8fCxM'></p>"
                    
#                     msg.html = htmlstr
                    
#                     with app.open_resource("invite_saveas.pdf") as fp:   #to attach a file
#                         msg.attach("invite.pdf", "application/pdf", fp.read()) #application/pdf is the mimetype for pdf
                    
#                     mail.send(msg)
#                     return "Email sent successfully" 
#                 except:  
#                     return "Connection Refused."    


#             else:
#                 flash('Please ensure the email address is correct.')
#         else: 
#             flash('Please input the email address associated to your account.')


@app.route('/forgot/password', methods=["POST","GET"])
def forgotpassword():
    if request.method == "GET":
        return redirect('/user/login/')
    else:
        email = request.form.get("forgotpw")

        if email:
            retrievedeets = db.session.query(User).filter(User.user_email==email).all()

            if retrievedeets:
                for i in retrievedeets:
                     retrievepw = i.user_pword

                    #  math.ceil(random.random() * 10000000000) 
               

                msg = Message('Hello', sender = 'samuelokediya@gmail.com', recipients = ['samuelokediya@gmail.com'])
                msg.body = f"This is your password {retrievepw}"
                mail.send(msg)
                return "Sent"



