import datetime
from sqlalchemy import Integer, Enum
from enum import unique
from Housemeapp import db


class User(db.Model): 
    user_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    user_email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(255), nullable=False)
    user_fname = db.Column(db.String(255), nullable=False)
    user_lname = db.Column(db.String(255), nullable=False)
    user_phone = db.Column(db.String(255), nullable=False)
    user_pword = db.Column(db.String(255), nullable=False)
    user_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    #relationships
    userpreferred = db.relationship('Preferred_property', back_populates ='user')
    
    
class Property_owner(db.Model): 
    owner_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    owner_email = db.Column(db.String(255), nullable=False, unique=True)
    owner_username = db.Column(db.String(255), nullable=False)
    owner_fname = db.Column(db.String(255), nullable=False)
    owner_lname = db.Column(db.String(255), nullable=False)
    owner_phone = db.Column(db.String(255), nullable=False)
    owner_pword = db.Column(db.String(255), nullable=False)
    owner_reg = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    #relationships
    owner =  db.relationship('Property', back_populates ='propertyowner') 
    propertyownerid = db.relationship('Owner_subscription', back_populates ='propowner') 
    

class Property(db.Model):
    property_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    property_address = db.Column(db.String(255), nullable=False)
    property_status = db.Column(db.Enum('Available','Unavailable'))
    property_price = db.Column(db.Numeric(14,2))
    property_description = db.Column(db.Text(), nullable=True)
    property_images =  db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    
    #foreign keys
    property_lgaid = db.Column(db.Integer(), db.ForeignKey("lga.lga_id")) 
    property_amenitiesid = db.Column(db.Integer(), db.ForeignKey("amenities.amenities_id")) 
    property_ownerid = db.Column(db.Integer(), db.ForeignKey("property_owner.owner_id")) 
    property_typeid = db.Column(db.Integer(), db.ForeignKey("property_type.type_id")) 
    #relationships 
    lgaarea = db.relationship('Lga', back_populates ='propertylga') 
    amenities = db.relationship('Amenities', back_populates ='propertyamenities') 
    propertyowner =  db.relationship('Property_owner', back_populates ='owner') 
    propertytype = db.relationship('Property_type', back_populates ='type')
    propertyid = db.relationship('Property_amenities', back_populates ='property') 
    preferredproperty = db.relationship('Preferred_property', back_populates ='property')
    propertyimages = db.relationship('Property_images', back_populates ='propertyidentity')  
    

class Property_amenities(db.Model):
    property_amenities_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    #foreign keys
    property_id = db.Column(db.Integer(), db.ForeignKey("property.property_id")) 
    amenities_id = db.Column(db.Integer(), db.ForeignKey("amenities.amenities_id")) 
    #relationships 
    property = db.relationship('Property', back_populates ='propertyid')
    amenities = db.relationship('Amenities', back_populates ='propamenities')
    

class Amenities(db.Model):
    amenities_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    amenities_name = db.Column(db.String(255), nullable=True)
    #relationships
    propertyamenities = db.relationship('Property', back_populates ='amenities') 
    propamenities = db.relationship('Property_amenities', back_populates ='amenities')
    
    
    
class Preferred_property(db.Model):
    preferred_property_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    #foreign keys
    property_id = db.Column(db.Integer(), db.ForeignKey("property.property_id")) 
    user_id = db.Column(db.Integer(), db.ForeignKey("user.user_id")) 
    #relationships 
    property = db.relationship('Property', back_populates ='preferredproperty')
    user = db.relationship('User', back_populates ='userpreferred')
    
    
class Lga(db.Model):
    lga_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    lga_name = db.Column(db.String(255), nullable=False)
    #foreign key
    state_id = db.Column(db.Integer(), db.ForeignKey("states.state_id"))
    #relationships
    propertylga = db.relationship('Property', back_populates ='lgaarea') 
    state = db.relationship('States', back_populates ='statelga')
    
    
    
class Property_images(db.Model):
    property_imageid = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    property_images =  db.Column(db.String(255), nullable=False)
    #foreign keys
    property_id = db.Column(db.Integer(), db.ForeignKey("property.property_id"))
    #relationship
    propertyidentity = db.relationship('Property', back_populates ='propertyimages')  
    

class Subscription_plan(db.Model):
    subscription_plan_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    subscription_plans = db.Column(db.Enum('Monthly','Yearly'))
    subscription_amount = db.Column(db.Enum('2000','24000'))
    #relationship
    subplan = db.relationship('Owner_subscription', back_populates ='subscription')
    

class States(db.Model):
    state_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    state_name = db.Column(db.String(255), nullable=False)
    #relationship
    statelga = db.relationship('Lga', back_populates ='state')
    

class Property_type(db.Model):
    type_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    property_name = db.Column(db.String(255), nullable=False)
    #relationships
    type = db.relationship('Property', back_populates ='propertytype') 
    

class Owner_subscription(db.Model):
    subscription_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    subscription_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    payment_ref = db.Column(db.String(255), nullable=False, unique =True)
    subscription_status = db.Column(db.Enum('Active','Inactive'))
    #foreign key
    property_ownerid = db.Column(db.Integer(), db.ForeignKey("property_owner.owner_id"))
    subscription_planid = db.Column(db.Integer(), db.ForeignKey("subscription_plan.subscription_plan_id"))
    #relationships
    propowner = db.relationship('Property_owner', back_populates ='propertyownerid') 
    subscription = db.relationship('Subscription_plan', back_populates ='subplan')
    
    
class Admin(db.Model): 
    admin_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    admin_username = db.Column(db.String(255), nullable=False)
    admin_password = db.Column(db.String(255), nullable=False)
    admin_lastlogin = db.Column(db.DateTime(), onupdate=datetime.datetime.utcnow())
    
    
    
    
    
    
    
    
    
  
    
    
    


    