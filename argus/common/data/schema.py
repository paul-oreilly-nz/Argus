import colander


class CPULoad(colander.SequenceSchema):
    load_percentage = colander.SchemaNode(
        colander.Int(), validator=colander.Range(0, 100)
    )


class CPUTimes(colander.MappingSchema):
    """Below values are multipled by 100 for tranmission to easier 'round' to ints"""

    user = colander.SchemaNode(colander.Decimal(quant="0.01"))
    nice = colander.SchemaNode(colander.Decimal(quant="0.01"))
    system = colander.SchemaNode(colander.Decimal(quant="0.01"))
    idle = colander.SchemaNode(colander.Decimal(quant="0.01"))
    iowait = colander.SchemaNode(colander.Decimal(quant="0.01"))
    irq = colander.SchemaNode(colander.Decimal(quant="0.01"))
    softirq = colander.SchemaNode(colander.Decimal(quant="0.01"))
    steal = colander.SchemaNode(colander.Decimal(quant="0.01"))
    guest = colander.SchemaNode(colander.Decimal(quant="0.01"))
    guest_nice = colander.SchemaNode(colander.Decimal(quant="0.01"))


class CPUs(colander.MappingSchema):
    load = CPULoad()
    times = CPUTimes()


class Heartbeat(colander.MappingSchema):
    timestamp = colander.DateTime()
    cpus = CPUs()


def full_colander_set():
    return {
        "cpu_load": CPULoad(),
        "cpu_times": CPUTimes(),
        "cpus": CPUs(),
        "heartbeat": Heartbeat(),
    }
