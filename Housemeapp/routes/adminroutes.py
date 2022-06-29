import math, random, os
from flask import render_template, request, abort, redirect, flash, make_response, session
from Housemeapp.mymodels import Admin, Property
from Housemeapp import app,db
from Housemeapp.mymodels import Amenities, Property_owner, Property_type, User, States, Lga, Property, Property_amenities, Property_images
# from Housemeapp.mymodels import User,State
# from Housemeapp.forms import LoginForm

@app.route('/admin/login/')
def adminlogin():
    return render_template('admin/adminlogin.html')
    
   
@app.route('/admin/loginverification/',methods=['GET','POST'])
def verifyadmin():
    if request.method == 'GET':
        return redirect('/admin/login/')
    else:
        adminusername = request.form.get('adminusername')
        adminpassword = request.form.get('adminpwd')
        if adminusername !='' or adminpassword !='':
            admindeets= db.session.query(Admin).filter(Admin.admin_username==adminusername, Admin.admin_password==adminpassword).first()
            if admindeets:
                session['admin'] = admindeets.admin_id
                return render_template('admin/admindashboard.html', admindeets=admindeets)
            else:
                flash('Please ensure the details are correctly filled')
                return redirect('/admin/login/')
        else:
            flash('Please ensure all fields are filled')
            return redirect('/admin/login/')
    
    
    
@app.route('/admin/logout')
def adminlogout():
    session.pop('admin')
    return redirect('/admin/login/')


@app.route('/admin/dashboard/')
def admindashboard():
    Adminlogged = session.get('admin')
    if Adminlogged ==None:
        return redirect('/admin/login/')
    else:
        return render_template("admin/admindashboard.html")
    
@app.route('/admin/allproperties/')
def allproperties():
    Adminlogged = session.get('admin')
    if Adminlogged ==None:
        return redirect('/admin/login/')
    else:
        allproperties = db.session.query(Property).all()
        return render_template("admin/allproperties.html", allproperties=allproperties)
    
    
@app.route('/admin/delete/listing/<id>')
def admin_delete(id):
    Adminlogged = session.get('admin')
    if Adminlogged ==None:
        return redirect('admin/login/')
    else:
          b = db.session.query(Property).get(id)
          db.session.delete(b)
          db.session.commit()
          flash(f"The property located at {b.property_address} has been successfully deleted")
          return redirect('/admin/allproperties/')
    
    
    
@app.route('/admin/list/property')
def adminlist():
    Adminlogged = session.get('admin')
    if Adminlogged ==None:
        return redirect('/admin/login/')
    else:
        states = db.session.query(States).all()
        property = db.session.query(Property_type).all()
        lga = db.session.query(Lga).all()
        amenities = db.session.query(Amenities).all()
        return render_template('admin/adminlists.html', states=states, property=property,lga=lga, amenities=amenities)
      
      
        
@app.route('/admin/property/details', methods=['POST'])
def adminpropertydetails():
    
    Adminlogged = session.get('admin')
    if Adminlogged == None:
            return redirect('/admin/login/')
    else:
        propertytype = request.form.get('propertytype')
        price = request.form.get('price')
        address = request.form.get('address')
        state = request.form.get('state')
        lga = request.form.get('lga')
        amenities = request.form.getlist('amenities')
        description = request.form.get('description')
        propertyimages = request.files.get('images')
        
        admin = Admin.query.get(Adminlogged)
        
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
                 
                    
                 p = Property(property_price=price, property_description=description, property_typeid=propertytype, property_address=address, property_lgaid=lga, property_images=save_as, property_ownerid=Adminlogged)
                 db.session.add(p)
                 db.session.commit()   
                 
                 propid = db.session.query(Property).filter(Property.property_ownerid == Adminlogged).first()
                 
                 for a in amenities:
                     q = Property_amenities(property_id=propid.property_id, amenities_id=a)
                     db.session.add(q)
                 db.session.commit()
                 
                 flash('Details posted successfully')
                 return redirect('/admin/allproperties/')     
                
             else:
                flash('File Not Allowed')
                return redirect('/admin/list/property')
    
