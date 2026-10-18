// Cycle Meet engine - when do things that repeat on different periods line up again.
// Mirrored by oracle.py; keep the op order identical.
// Periods are whole numbers from 1 to 1000000, starts are whole numbers from 0 to 1000000, in any one unit of time.
// Arithmetic is exact (big integers).

function _int(x, label, min, max) {
  if (typeof x !== "number" || !isFinite(x) || Math.floor(x) !== x || x < min || x > max) {
    throw new Error(label + " must be a whole number from " + min + " to " + max);
  }
  return BigInt(x);
}

function _gcd(a, b) {
  while (b !== 0n) { var t = a % b; a = b; b = t; }
  return a;
}

function _cyc(k) { return k + (k === 1n ? " cycle" : " cycles"); }

// Inverse of a modulo m (a and m are coprime); 0 when m is 1.
function _inv(a, m) {
  if (m === 1n) return 0n;
  var r0 = m, r1 = a % m, t0 = 0n, t1 = 1n;
  while (r1 !== 0n) {
    var q = r0 / r1, r2 = r0 - q * r1, t2 = t0 - q * t1;
    r0 = r1; r1 = r2; t0 = t1; t1 = t2;
  }
  return ((t0 % m) + m) % m;
}

// The meet truth: two things that repeat every a and every b.
function meetTruth(a, b) {
  var x = _int(a, "first period", 1, 1000000), y = _int(b, "second period", 1, 1000000);
  var l = x / _gcd(x, y) * y;
  return "Something that repeats every " + a + " and something that repeats every " + b +
    " meet again every " + l + " (" + _cyc(l / x) + " of the first, " + _cyc(l / y) + " of the second).";
}

// The three truth: three things that repeat every a, b and c.
function threeTruth(a, b, c) {
  var x = _int(a, "first period", 1, 1000000), y = _int(b, "second period", 1, 1000000), z = _int(c, "third period", 1, 1000000);
  var l = x / _gcd(x, y) * y;
  l = l / _gcd(l, z) * z;
  return "Three things that repeat every " + a + ", " + b + " and " + c + " all meet again every " + l +
    " (" + _cyc(l / x) + " of the first, " + _cyc(l / y) + " of the second, " + _cyc(l / z) + " of the third).";
}

// The start truth: things that begin at different times, then repeat.
function startTruth(a, startA, b, startB) {
  var x = _int(a, "first period", 1, 1000000), s = _int(startA, "first start", 0, 1000000);
  var y = _int(b, "second period", 1, 1000000), u = _int(startB, "second start", 0, 1000000);
  var head = "Something that fires at " + startA + " and then every " + a + ", and something that fires at " + startB + " and then every " + b + ", ";
  var g = _gcd(x, y);
  var diff = u - s;
  if (diff % g !== 0n) {
    var gap = diff < 0n ? -diff : diff;
    return head + "never fire together: the starts differ by " + gap + ", which is not a multiple of " + g +
      ", the greatest common divisor of " + a + " and " + b + ".";
  }
  var l = x / g * y, m = y / g;
  var k = (((diff / g) % m + m) % m) * _inv((x / g) % m, m) % m;
  var t = s + x * k;
  t = ((t % l) + l) % l;
  var top = s > u ? s : u;
  if (t < top) t = t + ((top - t + l - 1n) / l) * l;
  return head + "first fire together at " + t + ", then every " + l + " after that.";
}
