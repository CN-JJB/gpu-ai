import Foundation
import Metal

func gib(_ bytes: UInt64) -> String {
    return String(format: "%.3f GiB", Double(bytes) / 1073741824.0)
}

func gibInt(_ bytes: Int) -> String {
    return String(format: "%.3f GiB", Double(bytes) / 1073741824.0)
}

guard let device = MTLCreateSystemDefaultDevice() else {
    fputs("No default Metal device\n", stderr)
    exit(2)
}

print("device.name = \(device.name)")
print("device.registryID = \(device.registryID)")
print("device.hasUnifiedMemory = \(device.hasUnifiedMemory)")
print("device.isLowPower = \(device.isLowPower)")
print("device.isRemovable = \(device.isRemovable)")
print("device.isHeadless = \(device.isHeadless)")
print("device.recommendedMaxWorkingSetSize = \(device.recommendedMaxWorkingSetSize) bytes (\(gib(device.recommendedMaxWorkingSetSize)))")
print("device.currentAllocatedSize = \(device.currentAllocatedSize) bytes (\(gibInt(device.currentAllocatedSize)))")
print("device.maxBufferLength = \(device.maxBufferLength) bytes (\(gibInt(device.maxBufferLength)))")

let source = """
#include <metal_stdlib>
using namespace metal;

kernel void course_noop(
    device float *x [[buffer(0)]],
    uint gid [[thread_position_in_grid]]) {
    if (gid == 0) {
        x[0] = x[0];
    }
}
"""

do {
    let library = try device.makeLibrary(source: source, options: nil)
    guard let function = library.makeFunction(name: "course_noop") else {
        fputs("Unable to create course_noop Metal function\n", stderr)
        exit(3)
    }
    let pipeline = try device.makeComputePipelineState(function: function)
    print("pipeline.threadExecutionWidth = \(pipeline.threadExecutionWidth)")
    print("pipeline.maxTotalThreadsPerThreadgroup = \(pipeline.maxTotalThreadsPerThreadgroup)")
    print("pipeline.staticThreadgroupMemoryLength = \(pipeline.staticThreadgroupMemoryLength) bytes")
} catch {
    fputs("Metal pipeline compile failed: \(error)\n", stderr)
    exit(4)
}
