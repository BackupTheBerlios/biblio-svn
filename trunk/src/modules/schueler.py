import database
db=database.Database()
   
class Pupil():
    def create(self):
        db.query('insert into pupil values()')
        pupilnr=db.query('select max(nr) from pupil')
        return pupilnr [0][0]

    def edit(self,nr,vorname,nachname,geburtsdatum,jahrgang):
        if(db.check("nr",nr) and db.check("text",vorname) and db.check("text",nachname) and db.check("text",geburtsdatum) and db.check("text",jahrgang)):
            if db.query('select nr from pupil where nr='+nr+'')!=():
                db.query('update pupil SET vor="'+vorname+'",nach="'+nachname+'",geb="'+geburtsdatum+'", jahrgang='+jahrgang+' where nr='+nr+'')
                return True
            else:
                raise ValueError,"Invalid Input or Pupilnumber doesn't exist"

    def exist(self,pupilnr):
        if db.check("nr",pupilnr):
            if db.query('select nr from pupil where nr='+pupilnr+''):
                return True
            else:
                raise ValueError,"Pupilnumber does not exist"

    def delete(self,pupilnr):
        if db.check("nr",pupilnr):
            if db.query ('select pnr from ausleihe where pnr='+str(pupilnr)+'')!=():
                raise ValueError,"Pupil has borrowed one or more books."
            else:
                if db.query ('select nr from pupil where nr='+str(pupilnr)+'')!=():
                    db.query ('delete from pupil where nr='+str(pupilnr)+'')
                    return True   
                else:
                    raise ValueError,"Invalid Pupilnumber."

    def info(self,pupilnr):
        info_dict=db.query('select nr, vor, nach, date_format(geb,"%e.%c.%Y"),jahrgang from pupil where nr='+str(pupilnr)+'')
        if len(info_dict)==0:
            raise ValueError,"Pupilnumber does not exist."

        return (info_dict)

if "__main__"==__name__:




#==================================================
#    schueler=Pupil()
#    print schueler.exist('11')
#    print schueler.create()
#    print schueler.edit("20","Micky","Mouse","1990-5-22","12")
#    print schueler.info(20)[0]
#    print schueler.delete('2')
#===============================================================================


#===============================================================================
#    print mach_kurz("1000013765")
#    print mach_lang("1434")
#===============================================================================>>>>>>> .r81
