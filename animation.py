from manim import *
import math

class SineCurveUnitCircle(Scene):
    # contributed by heejin_park, https://infograph.tistory.com/230
    def construct(self):
        self.show_axis()
        self.show_circle()
        self.move_dot_and_draw_curve()
        self.wait()

    def show_axis(self):
        x_start = np.array([-6,0,0])
        x_end = np.array([6,0,0])

        y_start = np.array([-4,-2,0])
        y_end = np.array([-4,2,0])

        x_axis = Line(x_start, x_end)
        y_axis = Line(y_start, y_end)

        self.add(x_axis, y_axis)
        self.add_x_labels()

        self.origin_point = np.array([-4,0,0])
        self.curve_start = np.array([-3,0,0])

    def add_x_labels(self):
        x_labels = [
            MathTex("\pi"), MathTex("2 \pi"),
            MathTex("3 \pi"), MathTex("4 \pi"),
        ]

        for i in range(len(x_labels)):
            x_labels[i].next_to(np.array([-1 + 2*i, 0, 0]), DOWN)
            self.add(x_labels[i])

    def show_circle(self):
        circle = Circle(radius=1)
        circle.move_to(self.origin_point)
        self.add(circle)
        self.circle = circle

    def move_dot_and_draw_curve(self):
        orbit = self.circle
        origin_point = self.origin_point

        dot = Dot(radius=0.08, color=YELLOW)
        dot.move_to(orbit.point_from_proportion(0))
        self.t_offset = 0
        rate = 0.25

        def go_around_circle(mob, dt):
            self.t_offset += (dt * rate)
            # print(self.t_offset)
            mob.move_to(orbit.point_from_proportion(self.t_offset % 1))

        def get_line_to_circle():
            return Line(origin_point, dot.get_center(), color=BLUE)

        def get_line_to_curve():
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            return Line(dot.get_center(), np.array([x,y,0]), color=YELLOW_A, stroke_width=2 )


        self.curve = VGroup()
        self.curve.add(Line(self.curve_start,self.curve_start))
        def get_curve():
            last_line = self.curve[-1]
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            new_line = Line(last_line.get_end(),np.array([x,y,0]), color=YELLOW_D)
            self.curve.add(new_line)

            return self.curve

        dot.add_updater(go_around_circle)

        origin_to_circle_line = always_redraw(get_line_to_circle)
        dot_to_curve_line = always_redraw(get_line_to_curve)
        sine_curve_line = always_redraw(get_curve)

        self.add(dot)
        self.add(orbit, origin_to_circle_line, dot_to_curve_line, sine_curve_line)
        self.wait(8.5)

        dot.remove_updater(go_around_circle)

class VectorTimes(Scene):
    def construct(self):
        plane = NumberPlane()
        vec1 = Vector([4,7])
        vec2 = Vector([16,28])
        self.add(plane, vec1)
        self.play(vec1.animate.transform(vec2, run_time=2))

class LinearTransformation(LinearTransformationScene, MovingCameraScene):
    def __init__(self):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=True,
        )

    def construct(self):
        matrix_tex = MathTex("A=\\begin{bmatrix}1 & 1 \\\\ 0 & 2\\end{bmatrix}").to_edge(UL).add_background_rectangle()
        unit_square = self.get_unit_square()
        matrix = [[1, 1], [0, 2]]
        self.add_transformable_mobject(unit_square)
        self.add_background_mobject(matrix_tex)
        self.apply_matrix(matrix)
        self.wait()


class Trans3D(ThreeDScene):

    CONFIG = {
        "x_axis_label": "$x$",
        "y_axis_label": "$y$",
        "basis_i_color": GREEN,
        "basis_j_color": RED,
        "basis_k_color": GOLD
    }

    def create_matrix(self, np_matrix):

        m = Matrix(np_matrix)

        m.scale(0.5)
        m.set_column_colors(GREEN, RED, GOLD)

        m.to_corner(UP + LEFT)

        return m

    def construct(self):

        M = np.array([
            [2, 2, -1],
            [-2, 1, 2],
            [3, 1, -0]
        ])

        axes = ThreeDAxes()
        axes.set_color(GRAY)
        axes.add(axes.get_axis_labels())

        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # basis vectors i,j,k
        basis_vector_helper = Tex("$i$", ",", "$j$", ",", "$k$")
        basis_vector_helper[0].set_color(GREEN)
        basis_vector_helper[2].set_color(RED)
        basis_vector_helper[4].set_color(GOLD)

        basis_vector_helper.to_corner(UP + RIGHT)

        self.add_fixed_in_frame_mobjects(basis_vector_helper)

        # matrix
        matrix = self.create_matrix(M)

        self.add_fixed_in_frame_mobjects(matrix)

        # axes & camera
        self.add(axes)

        self.begin_ambient_camera_rotation(rate=0.2)

        cube = Cube(side_length=1, fill_color=BLUE, stroke_width=2, fill_opacity=0.1)
        cube.set_stroke(BLUE_E)

        i_vec = Vector(np.array([1, 0, 0]), color=GREEN)
        j_vec = Vector(np.array([0, 1, 0]), color=RED)
        k_vec = Vector(np.array([0, 0, 1]), color=GOLD)

        i_vec_new = Vector(M @ np.array([1, 0, 0]), color=GREEN)
        j_vec_new = Vector(M @ np.array([0, 1, 0]), color=RED)
        k_vec_new = Vector(M @ np.array([0, 0, 1]), color=GOLD)

        self.play(
            GrowArrow(i_vec),
            GrowArrow(j_vec),
            GrowArrow(k_vec),
            Write(basis_vector_helper)
        )

        self.wait()

        matrix_anim = ApplyMatrix(M, cube)

        self.play(
            matrix_anim,
            Transform(i_vec, i_vec_new, rate_func=matrix_anim.get_rate_func(),
                      run_time=matrix_anim.get_run_time()),
            Transform(j_vec, j_vec_new, rate_func=matrix_anim.get_rate_func(),
                      run_time=matrix_anim.get_run_time()),
            Transform(k_vec, k_vec_new, rate_func=matrix_anim.get_rate_func(),
                      run_time=matrix_anim.get_run_time())
        )

        self.wait()

        self.wait(7)

class trans1(LinearTransformationScene):
    def __init__(self):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=True,
        )

    def construct(self):
        matrix_tex = MathTex("A=\\begin{bmatrix}0 & 1 \\\\ -2 & -3\\end{bmatrix}, \\vec{v} = \\begin{bmatrix}\\frac{1}{\\sqrt{2}} \\\\ -\\frac{1}{\\sqrt{2}} \\end{bmatrix}").to_edge(UL).add_background_rectangle()
        mult_tex = MathTex("A\\vec{v}=\\begin{bmatrix}0 & 1 \\\\ -2 & -3\\end{bmatrix}\\begin{bmatrix}\\frac{1}{\\sqrt{2}} \\\\ -\\frac{1}{\\sqrt{2}} \\end{bmatrix} = \\begin{bmatrix}-\\frac{1}{\\sqrt{2}} \\\\ \\frac{1}{\\sqrt{2}} \\end{bmatrix}").add_background_rectangle().to_edge(DL)
        matrix = [[0, 1], [-2, -3]]
        self.add_background_mobject(matrix_tex, mult_tex)
        vector = Vector([1/math.sqrt(2), -1/math.sqrt(2)], color=GOLD)
        self.add_transformable_mobject(vector)
        self.apply_matrix(matrix)
        self.wait()

class eigen1(Scene):
    def construct(self):
        tex = MathTex("\\lambda=-1, \\vec{v}=\\begin{bmatrix}\\frac{1}{\\sqrt{2}} \\\\ -\\frac{1}{\\sqrt{2}} \\end{bmatrix}").add_background_rectangle().to_edge(UL)
        mult_tex = MathTex("\\lambda\\vec{v}=\\begin{bmatrix}-\\frac{1}{\\sqrt{2}} \\\\ \\frac{1}{\\sqrt{2}} \\end{bmatrix}").add_background_rectangle().to_edge(DL)
        plane = NumberPlane()
        vec1 =  Vector([1/math.sqrt(2), -1/math.sqrt(2)], color=GOLD)
        vec2 = Vector([-1/math.sqrt(2), 1/math.sqrt(2)], color=GOLD)
        self.add(vec1, plane, tex, mult_tex)
        self.play(Transform(vec1, vec2))
        self.wait(2)

class trans2(LinearTransformationScene):
    def __init__(self):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=True,
        )

    def construct(self):
        matrix_tex = MathTex("A=\\begin{bmatrix}0 & 1 \\\\ -2 & -3\\end{bmatrix}, \\vec{v}=\\begin{bmatrix}-\\frac{1}{\\sqrt{5}} \\\\ \\frac{2}{\\sqrt{5}} \\end{bmatrix}").to_edge(UL).add_background_rectangle()
        mult_tex = MathTex("A\\vec{v}=\\begin{bmatrix}0 & 1 \\\\ -2 & -3\\end{bmatrix}\\begin{bmatrix}-\\frac{1}{\\sqrt{5}} \\\\ \\frac{2}{\\sqrt{5}} \\end{bmatrix} = \\begin{bmatrix}\\frac{2}{\\sqrt{5}} \\\\ -\\frac{4}{\\sqrt{5}} \\end{bmatrix}").add_background_rectangle().to_edge(DL)
        matrix = [[0, 1], [-2, -3]]
        self.add_background_mobject(matrix_tex, mult_tex)
        vector = Vector([-1/math.sqrt(5), 2/math.sqrt(5)], color=GOLD)
        self.add_transformable_mobject(vector)
        self.apply_matrix(matrix)
        self.wait()

class eigen2(Scene):
    def construct(self):
        tex = MathTex("\\lambda=-2, \\vec{v}=\\begin{bmatrix}-\\frac{1}{\\sqrt{5}} \\\\ \\frac{2}{\\sqrt{5}} \\end{bmatrix}").add_background_rectangle().to_edge(UL)
        mult_tex = MathTex("\\lambda\\vec{v}=\\begin{bmatrix}\\frac{2}{\\sqrt{5}} \\\\ -\\frac{4}{\\sqrt{5}} \\end{bmatrix}").add_background_rectangle().to_edge(DL)
        plane = NumberPlane()
        vec1 =  Vector([-1/math.sqrt(5), 2/math.sqrt(5)], color=GOLD)
        vec2 = Vector([2/math.sqrt(5), -4/math.sqrt(5)], color=GOLD)
        self.add(vec1, plane, tex, mult_tex)
        self.play(Transform(vec1, vec2))
        self.wait(2)