
function retval = dystrybuanta (x)
  if (0 <= x && x <= 1)
    retval = (x^2)/9;
    return
   elseif (1 < x && x <= 4)
    retval = (2*x - 1)/9;
    return
   elseif (4 < x && x <= 6)
    retval = (12*x - x^2 - 18)/18;
    return
   endif
   if(x < 0)
    retval = 0;
    return
   else
    retval = 1;
    return
  endif
endfunction