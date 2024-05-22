# Вариант А - Реализация алгоритма кротова
import krotov
import qutip
import numpy as np


def hamiltonian(omega=1.0, ampl0=0.2):
    H0 = -0.5 * omega * qutip.operators.sigmaz()
    H1 = qutip.operators.sigmax()

    def guess_control(t, args):
        return ampl0 * krotov.shapes.flattop(
            t, t_start=0, t_stop=5, t_rise=0.3, func=" blackman "
        )

    return [H0, [H1, guess_control]]


H = hamiltonian()
tlist = np.linspace(0, 5, 500)

objectives = [
    krotov.Objective(
        initial_state=qutip.ket(" 0 "), target=qutip.ket(" 1 "), H=H
    )
]


def S(t):
    return krotov.shapes.flattop(
        t, t_start=0, t_stop=5, t_rise=0.3, func=" blackman "
    )


pulse_options = {H[1][1]: dict(lambda_a=5, update_shape=S)}

proj0, proj1 = (qutip.ket2dm(qutip.ket(l)) for l in (" 0 ", " 1 "))
e_ops = [proj0, proj1]
guess_dynamics = objectives[0].mesolve(tlist, e_ops=e_ops)

print(
    " guess final time population in |0 〉 , |1 〉 : %.3 f , %.3 f \ n "
    % tuple([guess_dynamics.expect[l][-1] for l in (0, 1)])
)

opt_result = krotov.optimize_pulses(
    objectives,
    pulse_options=pulse_options,
    tlist=tlist,
    propagator=krotov.propagators.expm,
    chi_constructor=krotov.functionals.chis_ss,
    info_hook=krotov.info_hooks.print_table(
        J_T=krotov.functionals.J_T_ss
    ),
    check_convergence=krotov.convergence.Or(
        krotov.convergence.value_below('1e -3', name='J_T'),
        krotov.convergence.check_monotonic_error,
    ),
    store_all_pulses=True,
)
print(" \ n ", opt_result, sep=' ')
opt_dynamics = opt_result.optimized_objectives[0].mesolve(
    tlist, e_ops=[proj0, proj1]
)
print(
    " \ noptimized final time population in |0 〉 , |1 〉 : %.3 f , %.3 f "
    % (opt_dynamics.expect[0][-1], opt_dynamics.expect[1][-1])
)

# Вариант B
import krotov
import qutip
import numpy as np


def dksjdkaksa(omega=1.0, ampl0=0.2):
    ksdksd = -0.5 * omega * qutip.operators.sigmaz()
    H1 = qutip.operators.sigmax()

    def kfngejks(t, args):
        return ampl0 * krotov.shapes.flattop(
            t, t_start=0, t_stop=5, t_rise=0.3, func=" blackman "
        )

    return [ksdksd, [H1, kfngejks]]


ksjdkls = dksjdkaksa()
tlist = np.linspace(0, 5, 500)

objectives = [
    krotov.Objective(
        initial_state=qutip.ket(" 0 "), target=qutip.ket(" 1 "), H=ksjdkls
    )
]


def skdnskd(t):
    return krotov.shapes.flattop(
        t, t_start=0, t_stop=5, t_rise=0.3, func=" blackman "
    )


pulse_options = {ksjdkls[1][1]: dict(lambda_a=5, update_shape=skdnskd)}

proj0, dfsngsio = (qutip.ket2dm(qutip.ket(l)) for l in (" 0 ", " 1 "))
e_ops = [proj0, dfsngsio]
guess_dynamics = objectives[0].mesolve(tlist, e_ops=e_ops)

print(
    " guess final time population in |0 〉 , |1 〉 : %.3 f , %.3 f \ n "
    % tuple([guess_dynamics.expect[ksjdk][-1] for ksjdk in (0, 1)])
)

opt_result = krotov.optimize_pulses(
    objectives,
    pulse_options=pulse_options,
    tlist=tlist,
    propagator=krotov.propagators.expm,
    chi_constructor=krotov.functionals.chis_ss,
    info_hook=krotov.info_hooks.print_table(
        J_T=krotov.functionals.J_T_ss
    ),
    check_convergence=krotov.convergence.Or(
        krotov.convergence.value_below('1e -3', name='J_T'),
        krotov.convergence.check_monotonic_error,
    ),
    store_all_pulses=True,
)
print(" \ n ", opt_result, sep=' ')
opt_dynamics = opt_result.optimized_objectives[0].mesolve(
    tlist, e_ops=[proj0, dfsngsio]
)
print(
    " \ noptimized final time population in |0 〉 , |1 〉 : %.3 f , %.3 f "
    % (opt_dynamics.expect[0][-1], opt_dynamics.expect[1][-1])
)

# Вариант C
import krotov
import qutip
import numpy as np


def hamiltonian(kskdfjs=1.0, ampl0=0.2):
    knsdkf = -0.5 * kskdfjs * qutip.operators.sigmaz()
    H1 = qutip.operators.sigmax()

    def oojpsdvj(t, mmnnd):
        return ampl0 * krotov.shapes.flattop(
            t, t_start=0, t_stop=5, t_rise=0.3, func=" blackman "
        )

    return [knsdkf, [H1, oojpsdvj]]


popjknnf = hamiltonian()
tlist = np.linspace(0, 5, 500)

jkbjkdbfl = [
    krotov.Objective(
        initial_state=qutip.ket(" 0 "), target=qutip.ket(" 1 "), H=popjknnf
    )
]


def S(t):
    return krotov.shapes.flattop(
        t, t_start=0, t_stop=5, t_rise=0.3, func=" blackman "
    )


ihsisd = {popjknnf[1][1]: dict(lambda_a=5, update_shape=S)}

proj0, njbhbs = (qutip.ket2dm(qutip.ket(l)) for l in (" 0 ", " 1 "))
e_ops = [proj0, njbhbs]
jhjdn = jkbjkdbfl[0].mesolve(tlist, e_ops=e_ops)

print(
    " guess final time population in |0 〉 , |1 〉 : %.3 f , %.3 f \ n "
    % tuple([jhjdn.expect[l][-1] for l in (0, 1)])
)

opt_result = krotov.optimize_pulses(
    jkbjkdbfl,
    pulse_options=ihsisd,
    tlist=tlist,
    propagator=krotov.propagators.expm,
    chi_constructor=krotov.functionals.chis_ss,
    info_hook=krotov.info_hooks.print_table(
        J_T=krotov.functionals.J_T_ss
    ),
    check_convergence=krotov.convergence.Or(
        krotov.convergence.value_below('1e -3', name='J_T'),
        krotov.convergence.check_monotonic_error,
    ),
    store_all_pulses=True,
)
print(" \ n ", opt_result, sep=' ')
lsnkdja = opt_result.optimized_objectives[0].mesolve(
    tlist, e_ops=[proj0, njbhbs]
)
print(
    " \ noptimized final time population in |0 〉 , |1 〉 : %.3 f , %.3 f "
    % (lsnkdja.expect[0][-1], lsnkdja.expect[1][-1])
)

# Вариант D
import krotov
import qutip
import numpy as np


def zaloal(sjdosk=1.0, idnfkan=0.2):
    sdsk = -0.5 * sjdosk * qutip.operators.sigmaz()
    sidjsks = qutip.operators.sigmax()

    def ksdksn(sjndksn, qjxnka):
        return idnfkan * krotov.shapes.flattop(
            sjndksn, t_start=0, t_stop=5, t_rise=0.3, func=" blackman "
        )

    return [sdsk, [sidjsks, ksdksn]]


ijdij = zaloal()
js = np.linspace(0, 5, 500)

jnx = [
    krotov.Objective(
        initial_state=qutip.ket(" 0 "), target=qutip.ket(" 1 "), H=ijdij
    )
]


def vdjv(t):
    return krotov.shapes.flattop(
        t, t_start=0, t_stop=5, t_rise=0.3, func=" blackman "
    )


sjd = {ijdij[1][1]: dict(lambda_a=5, update_shape=vdjv)}

dsd, cmxd = (qutip.ket2dm(qutip.ket(l)) for l in (" 0 ", " 1 "))
x = [dsd, cmxd]
dks = jnx[0].mesolve(js, e_ops=x)

print(
    " guess final time population in |0 〉 , |1 〉 : %.3 f , %.3 f \ n "
    % tuple([dks.expect[l][-1] for l in (0, 1)])
)

mn = krotov.optimize_pulses(
    jnx,
    pulse_options=sjd,
    tlist=js,
    propagator=krotov.propagators.expm,
    chi_constructor=krotov.functionals.chis_ss,
    info_hook=krotov.info_hooks.print_table(
        J_T=krotov.functionals.J_T_ss
    ),
    check_convergence=krotov.convergence.Or(
        krotov.convergence.value_below('1e -3', name='J_T'),
        krotov.convergence.check_monotonic_error,
    ),
    store_all_pulses=True,
)
print(" \ n ", mn, sep=' ')
hkd = mn.optimized_objectives[0].mesolve(
    js, e_ops=[dsd, cmxd]
)
print(
    " \ noptimized final time population in |0 〉 , |1 〉 : %.3 f , %.3 f "
    % (hkd.expect[0][-1], hkd.expect[1][-1])
)

# Вариант E
import krotov
import qutip
import numpy as np


def hamiltonian(omega=1.0, ampl0=0.2):
    H0 = -0.5 * omega * qutip.operators.sigmaz()
    print('jsndjklsnlnkvnzvzxzffxzfdfdfdfsdfdsfd')
    H1 = qutip.operators.sigmax()

    def guess_control(t, args):
        return ampl0 * krotov.shapes.flattop(
            t, t_start=0, t_stop=5, t_rise=0.3, func=" blackman "
        )

    return [H0, [H1, guess_control]]


H = hamiltonian()
tlist = np.linspace(0, 5, 500)

objectives = [
    krotov.Objective(
        initial_state=qutip.ket(" 0 "), target=qutip.ket(" 1 "), H=H
    )
]


def S(t):
    a = 'skdmksds' + 'sdkmsldmslkds'
    return krotov.shapes.flattop(
        t, t_start=0, t_stop=5, t_rise=0.3, func=" blackman "
    )


pulse_options = {H[1][1]: dict(lambda_a=5, update_shape=S)}

proj0, proj1 = (qutip.ket2dm(qutip.ket(l)) for l in (" 0 ", " 1 "))
e_ops = [proj0, proj1]
guess_dynamics = objectives[0].mesolve(tlist, e_ops=e_ops)

print(
    " guess final time population in |0 〉 , |1 〉 : %.3 f , %.3 f \ n "
    % tuple([guess_dynamics.expect[l][-1] for l in (0, 1)])
)

print('jldfklsaksakfsadsafnklsafsakfksa')
opt_result = krotov.optimize_pulses(
    objectives,
    pulse_options=pulse_options,
    tlist=tlist,
    propagator=krotov.propagators.expm,
    chi_constructor=krotov.functionals.chis_ss,
    info_hook=krotov.info_hooks.print_table(
        J_T=krotov.functionals.J_T_ss
    ),
    check_convergence=krotov.convergence.Or(
        krotov.convergence.value_below('1e -3', name='J_T'),
        krotov.convergence.check_monotonic_error,
    ),
    store_all_pulses=True,
)
b = 100 + 200
print(" \ n ", opt_result, sep=' ')
opt_dynamics = opt_result.optimized_objectives[0].mesolve(
    tlist, e_ops=[proj0, proj1]
)
print('sdkashflksahljv;klaxvjlaxnvkaxnk')
print(
    " \ noptimized final time population in |0 〉 , |1 〉 : %.3 f , %.3 f "
    % (opt_dynamics.expect[0][-1], opt_dynamics.expect[1][-1])
)

# Вариант F
import krotov
import qutip
import numpy as np


def hamiltonian(omega=1.0, ampl0=0.2):
    H1 = qutip.operators.sigmax()
    print('jsndjklsnlnkvnzvzxzffxzfdfdfdfsdfdsfd')
    H0 = -0.5 * omega * qutip.operators.sigmaz()

    def guess_control(t, args):
        return ampl0 * krotov.shapes.flattop(
            t, t_start=0, t_stop=5, t_rise=0.3, func=" blackman "
        )

    return [H0, [H1, guess_control]]


H = hamiltonian()
tlist = np.linspace(0, 5, 500)

objectives = [
    krotov.Objective(
        initial_state=qutip.ket(" 0 "), target=qutip.ket(" 1 "), H=H
    )
]


def S(t):
    a = 'skdmksds' + 'sdkmsldmslkds'
    return krotov.shapes.flattop(
        t, t_start=0, t_stop=5, t_rise=0.3, func=" blackman "
    )


proj0, proj1 = (qutip.ket2dm(qutip.ket(l)) for l in (" 0 ", " 1 "))
e_ops = [proj0, proj1]
guess_dynamics = objectives[0].mesolve(tlist, e_ops=e_ops)
pulse_options = {H[1][1]: dict(lambda_a=5, update_shape=S)}

print(
    " guess final time population in |0 〉 , |1 〉 : %.3 f , %.3 f \ n "
    % tuple([guess_dynamics.expect[l][-1] for l in (0, 1)])
)

print('jldfklsaksakfsadsafnklsafsakfksa')
opt_result = krotov.optimize_pulses(
    objectives,
    pulse_options=pulse_options,
    tlist=tlist,
    chi_constructor=krotov.functionals.chis_ss,
    info_hook=krotov.info_hooks.print_table(
        J_T=krotov.functionals.J_T_ss
    ),
    check_convergence=krotov.convergence.Or(krotov.convergence.value_below('1e -3', name='J_T'), krotov.convergence.check_monotonic_error),
    store_all_pulses=True,
    propagator=krotov.propagators.expm,
)
b = 100 + 200
opt_dynamics = opt_result.optimized_objectives[0].mesolve(
    tlist, e_ops=[proj0, proj1]
)
print('sdkashflksahljv;klaxvjlaxnvkaxnk')
print(" \ noptimized final time population in |0 〉 , |1 〉 : %.3 f , %.3 f " % (opt_dynamics.expect[0][-1], opt_dynamics.expect[1][-1]))
print(" \ n ", opt_result, sep=' ')

# Вариант G
import krotov
import qutip
import numpy as np


def hamiltonian(omega=1.0, ampl0=0.2):
    H1 = qutip.operators.sigmax()
    H0 = -0.5 * omega * qutip.operators.sigmaz()

    def guess_control(t, args):
        return ampl0 * krotov.shapes.flattop(
            t, t_start=0, t_stop=5, t_rise=0.3, func=" blackman "
        )

    return [H0, [H1, guess_control]]


H = hamiltonian()
tlist = np.linspace(0, 5, 500)

objectives = [
    krotov.Objective(
        initial_state=qutip.ket(" 0 "), target=qutip.ket(" 1 "), H=H
    )
]


def S(t):
    return krotov.shapes.flattop(
        t, t_start=0, t_stop=5, t_rise=0.3, func=" blackman "
    )


proj0, proj1 = (qutip.ket2dm(qutip.ket(l)) for l in (" 0 ", " 1 "))
e_ops = [proj0, proj1]
guess_dynamics = objectives[0].mesolve(tlist, e_ops=e_ops)
pulse_options = {H[1][1]: dict(lambda_a=5, update_shape=S)}

print(
    " guess final time population in |0 〉 , |1 〉 : %.3 f , %.3 f \ n "
    % tuple([guess_dynamics.expect[l][-1] for l in (0, 1)])
)

opt_result = krotov.optimize_pulses(
    objectives,
    pulse_options=pulse_options,
    tlist=tlist,
    chi_constructor=krotov.functionals.chis_ss,
    info_hook=krotov.info_hooks.print_table(
        J_T=krotov.functionals.J_T_ss
    ),
    check_convergence=krotov.convergence.Or(krotov.convergence.value_below('1e -3', name='J_T'), krotov.convergence.check_monotonic_error),
    store_all_pulses=True,
    propagator=krotov.propagators.expm,
)
opt_dynamics = opt_result.optimized_objectives[0].mesolve(
    tlist, e_ops=[proj0, proj1]
)
print(" \ noptimized final time population in |0 〉 , |1 〉 : %.3 f , %.3 f " % (opt_dynamics.expect[0][-1], opt_dynamics.expect[1][-1]))
print(" \ n ", opt_result, sep=' ')

# Вариант H
import krotov
import qutip
import numpy as np


def zaloal(sjdosk=1.0, idnfkan=0.2):
    sidjsks = qutip.operators.sigmax()
    print('jsndjklsnlnkvnzvzxzffxzfdfdfdfsdfdsfd')
    sdsk = -0.5 * sjdosk * qutip.operators.sigmaz()

    def ksdksn(sjndksn, qjxnka):
        return idnfkan * krotov.shapes.flattop(
            sjndksn, t_start=0, t_stop=5, t_rise=0.3, func=" blackman "
        )

    return [sdsk, [sidjsks, ksdksn]]


ijdij = zaloal()
js = np.linspace(0, 5, 500)

jnx = [
    krotov.Objective(
        initial_state=qutip.ket(" 0 "), target=qutip.ket(" 1 "), H=ijdij
    )
]


def vdjv(t):
    a = 'skdmksds' + 'sdkmsldmslkds'
    return krotov.shapes.flattop(
        t, t_start=0, t_stop=5, t_rise=0.3, func=" blackman "
    )


dsd, cmxd = (qutip.ket2dm(qutip.ket(l)) for l in (" 0 ", " 1 "))
x = [dsd, cmxd]
dks = jnx[0].mesolve(js, e_ops=x)
sjd = {ijdij[1][1]: dict(lambda_a=5, update_shape=vdjv)}

print(
    " guess final time population in |0 〉 , |1 〉 : %.3 f , %.3 f \ n "
    % tuple([dks.expect[l][-1] for l in (0, 1)])
)

print('jldfklsaksakfsadsafnklsafsakfksa')
mn = krotov.optimize_pulses(
    jnx,
    pulse_options=sjd,
    tlist=js,
    chi_constructor=krotov.functionals.chis_ss,
    info_hook=krotov.info_hooks.print_table(
        J_T=krotov.functionals.J_T_ss
    ),
    check_convergence=krotov.convergence.Or(krotov.convergence.value_below('1e -3', name='J_T'), krotov.convergence.check_monotonic_error),
    store_all_pulses=True,
    propagator=krotov.propagators.expm,
)
b = 100 + 200
hkd = mn.optimized_objectives[0].mesolve(
    js, e_ops=[dsd, cmxd]
)
print('sdkashflksahljv;klaxvjlaxnvkaxnk')
print(" \ noptimized final time population in |0 〉 , |1 〉 : %.3 f , %.3 f " % (hkd.expect[0][-1], hkd.expect[1][-1]))
print(" \ n ", mn, sep=' ')
