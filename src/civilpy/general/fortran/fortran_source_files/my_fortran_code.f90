   module fortran_dll
   use iso_c_binding
   implicit none

   contains

   subroutine add_numbers(x, y, result) bind(c)
       real(c_double), value :: x, y  ! `value` makes the arguments passed by value
       real(c_double) :: result       ! This will store the result
       result = x + y
   end subroutine add_numbers

   subroutine multiply_numbers(x, y, result) bind(c)
       real(c_double), value :: x, y
       real(c_double) :: result
       result = x * y
   end subroutine multiply_numbers
   end module fortran_dll