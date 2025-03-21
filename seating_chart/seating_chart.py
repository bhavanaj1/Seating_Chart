from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import cairo, random
from django.conf import settings
import os


class SeatingChart:
    rectangles = os.path.join(settings.STATICFILES_DIRS[0], 'images/rectangles.svg')
    # rectangles = "/static/images/rectangles.svg"
    num_section = 0
    desk_in_row = 0
    desk_in_column = 0
    shuffle = True
    width = 0
    height = 0
    student_names = ""
    place_name_list = []

    def __init__(self, num_section, desk_in_row, desk_in_column, shuffle, student_names):
        self.num_section = num_section
        self.desk_in_row = desk_in_row
        self.desk_in_column = desk_in_column
        self.shuffle = shuffle
        self.width = desk_in_row * 460
        self.height = desk_in_column * 350 * num_section
        self.student_names = student_names

    def create_chart(self):
        with cairo.SVGSurface(self.rectangles, self.width, self.height) as surface:
            context = cairo.Context(surface)
            context.set_source_rgba(0, 0, 0, 1)

            def find_space_name(name, x, y):
                if " " in name:
                    space = name.find(" ")
                    context.stroke()
                    context.move_to(x, y+35)
                    context.show_text(name[0:space])
                    context.stroke()
                    context.move_to(x, y+65)
                    context.show_text(name[space+1:])
                elif len(name) >= 12:
                    context.stroke()
                    context.move_to(x, y+35)
                    context.show_text(name[0:11] + "-")
                    context.stroke()
                    context.move_to(x, y+65)
                    context.show_text(name[11:])
                else:
                    context.stroke()
                    context.move_to(x, y+35)
                    context.show_text(name)

            #first and last name
            def desk_name(x, y, name, placement):
                context.move_to(x,y-15)
                context.set_font_size(25)
                context.select_font_face("Arial")
                find_space_name(name[0], x, y-65)
                find_space_name(name[1], x, y)
                context.move_to(x, y+115)
                context.show_text(placement)

            #rectangle
            def rectangle_desk(x, y, x_dash, y_dash):
                context.set_line_width(10)
                context.set_dash([])
                context.rectangle(x, y, 400, 200) #(x, y, width, height)
                context.set_line_join(cairo.LINE_JOIN_BEVEL)
                context.stroke()
                context.set_dash([10.0])
                context.move_to(x_dash, y_dash) #(where,length of line)
                context.line_to(x_dash, y_dash - 200)
                context.stroke()

            # VARIABLES
            sections = "abcdefghijklmnopqurstuvwxyz"
            if self.shuffle == True:
                random.shuffle(self.student_names)
            placement_num_ltr = [1, sections[0].upper()]
            if self.num_section == 1:
                placement_num_ltr[1] = " "

            x_desk = 30
            y_desk = 90
            x_dash = 225
            y_dash = 285
            x_name = 50
            y_name = 160

            for section in range(self.num_section):
                if self.student_names == 0:
                    break
                placement_num_ltr[0] = 1
                placement_num_ltr[1] = sections[section].upper()
                if self.num_section == 1:
                    placement_num_ltr[1] = " "
                if section == 0:
                    context.move_to(30,60)
                    context.set_font_size(50)
                else:
                    y_name += 100
                context.show_text("Section "+ str(sections[section].upper()))
                for column in range(self.desk_in_column):
                    for desk in range(self.desk_in_row):
                        rectangle_desk(x_desk, y_desk, x_dash, y_dash)
                        x_desk += 450
                        x_dash += 450

                    for name in range(self.desk_in_row*2):
                        if self.student_names != []:
                            name_pop = self.student_names.pop(0)
                            desk_name(x_name, y_name, name_pop, str(placement_num_ltr[0]))
                            self.place_name_list.append([[name_pop[1], name_pop[0]], placement_num_ltr[0], placement_num_ltr[1]])
                            placement_num_ltr[0] += 1
                            x_name += 200
                            if name % 2:
                                x_name += 50
                    x_dash = 225
                    x_desk = 30
                    x_name = 50
                    y_desk += 250
                    y_dash += 250
                    y_name += 250

                y_desk += 100
                y_dash += 100
                y_name += 0
                context.move_to(30, y_name)
                context.set_font_size(50)

            context.stroke()
            print("chart created!")

    def make_pdf(self):
        pdf = canvas.Canvas(os.path.join(settings.STATICFILES_DIRS[0], 'images/Roster2.pdf'), pagesize=letter)
        pdf.setTitle("Roster2")
        text = pdf.beginText(40, 750)
        count = 0
        for line in range(len(self.place_name_list)):
            text.textLine(str(self.place_name_list[line][0][0]) + ", " + str(self.place_name_list[line][0][1]) + " " + str(self.place_name_list[line][1]) + str(self.place_name_list[line][2]))
            count+=1
            if line % 50 == 0 and line != 0:
                pdf.drawText(text)
                pdf.showPage()
                text = pdf.beginText(40, 750)
        pdf.drawText(text)
        pdf.save()

        self.place_name_list.sort()

        pdf2 = canvas.Canvas(os.path.join(settings.STATICFILES_DIRS[0], 'images/Roster.pdf'), pagesize=letter)
        pdf2.setTitle("Roster")
        text = pdf2.beginText(40, 750)
        count = 0
        for line in range(len(self.place_name_list)):
            text.textLine(str(self.place_name_list[line][0][0]) + ", " + str(self.place_name_list[line][0][1]) + " " + str(self.place_name_list[line][1]) + str(self.place_name_list[line][2]))
            count+=1
            if line % 50 == 0 and line != 0:
                pdf2.drawText(text)
                pdf2.showPage()
                text = pdf2.beginText(40, 750)
        pdf2.drawText(text)
        pdf2.save()
        print("pdfs created!")


#with open('static/US_Gov_Main_Gym.csv', 'r') as file:
#          csvreader = csv.reader(file)
#          new_student_name = []
#          for row in csvreader:
#                first_name = row[0]
#                last_name = row[1]
#                new_student_name.append([first_name.title(), last_name.title()])

#chart = SeatingChart(1, 10, 12, True, new_student_name)
#chart.create_chart()
#chart.make_pdf()









